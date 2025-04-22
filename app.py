from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from fpdf import FPDF
import io

app = Flask(__name__)
CORS(app)

@app.route("/enroll", methods=["POST"])
def enroll():
    try:
        data = request.json
        name = data.get("name")
        course = data.get("course")
        college = data.get("college")
        country = data.get("country")

        if not all([name, course, college, country]):
            return jsonify({"success": False, "message": "Missing fields"}), 400

        # Generate PDF using fpdf
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="Enrollment Confirmation", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
        pdf.cell(200, 10, txt=f"Course: {course}", ln=True)
        pdf.cell(200, 10, txt=f"College: {college}", ln=True)
        pdf.cell(200, 10, txt=f"Country: {country}", ln=True)

        # Save to in-memory buffer
        buffer = io.BytesIO()
        pdf.output(buffer)
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype="application/pdf",
            download_name="Enrollment_Confirmation.pdf",
            as_attachment=True
        )

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
