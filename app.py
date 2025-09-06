import os
import logging
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename

# -----------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "instance", "uploads")
ALLOWED_EXTENSIONS = {"pdf"}

# Ensure uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "super-secret-key"

# -----------------------------------------------------
# LOGGING CONFIGURATION
# -----------------------------------------------------
log_file = os.path.join(BASE_DIR, "app.log")
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# -----------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_h5p(input_pdf_path, dpi, resolution, output_dir):
    """Run generateh5p.py and return True if successful."""
    try:
        cmd = [
            "python3",
            "generateh5p.py",
            input_pdf_path,
            "--dpi", str(dpi),
            "--resolution", str(resolution),
            "--webOutput", output_dir,
        ]

        logger.info(f"Running command: {' '.join(cmd)}")
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        logger.debug(f"STDOUT:\n{process.stdout}")
        logger.debug(f"STDERR:\n{process.stderr}")

        if process.returncode != 0:
            logger.error(f"generateh5p.py failed with exit code {process.returncode}")
            return False

        return True

    except Exception as e:
        logger.exception(f"Exception while running generateh5p.py: {e}")
        return False

# -----------------------------------------------------
# ROUTES
# -----------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        # Ensure the form field name matches index.html
        if "my_pdf_file" not in request.files:
            flash("No file part in the request.")
            return redirect(request.url)

        file = request.files["my_pdf_file"]
        if file.filename == "":
            flash("No file selected.")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            logger.info(f"Uploaded PDF saved at: {file_path}")

            # Get additional params from the form
            dpi = request.form.get("dpi", 600)
            resolution = request.form.get("resolution", 1920)

            # Run H5P generation
            success = generate_h5p(file_path, dpi, resolution, app.config["UPLOAD_FOLDER"])

            h5p_filename = os.path.splitext(filename)[0] + ".h5p"
            h5p_path = os.path.join(app.config["UPLOAD_FOLDER"], h5p_filename)
            out_h5p_path = os.path.join(app.config["UPLOAD_FOLDER"], "out.h5p")

            if success and os.path.exists(h5p_path):
                os.replace(h5p_path, out_h5p_path)
                logger.info(f"Generated H5P saved at: {out_h5p_path}")
                return render_template("index.html", prediction=True, file_name=out_h5p_path)
            else:
                logger.error("H5P generation failed or file missing.")
                flash("Failed to generate H5P file. Check logs for details.")
                return redirect(url_for("index"))

        else:
            flash("Invalid file format. Please upload a PDF.")
            return redirect(url_for("index"))

    except Exception as e:
        logger.exception(f"Error in /submit: {e}")
        flash("Unexpected error occurred. Check logs.")
        return redirect(url_for("index"))


@app.route("/download", methods=["GET"])
def download():
    try:
        out_h5p_path = os.path.join(app.config["UPLOAD_FOLDER"], "out.h5p")
        if not os.path.exists(out_h5p_path):
            logger.error("Attempted to download non-existent H5P file.")
            flash("H5P file not found. Please regenerate.")
            return redirect(url_for("index"))

        logger.info("H5P file downloaded successfully.")
        return send_file(out_h5p_path, as_attachment=True)

    except Exception as e:
        logger.exception(f"Error in /download: {e}")
        return "Internal Server Error", 500


# -----------------------------------------------------
# MAIN ENTRY POINT
# -----------------------------------------------------
if __name__ == "__main__":
    logger.info("Starting Flask server...")
    app.run(host="127.0.0.1", port=8000, debug=True)
