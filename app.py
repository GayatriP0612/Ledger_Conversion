from __future__ import annotations
from pdfminer.layout import LTTextBoxHorizontal
import pandas as pd
import csv
from pdfminer.high_level import extract_pages
import streamlit as st
import tempfile
import os

# Streamlit page configuration
st.set_page_config(page_title="BE Marks Parser", page_icon="📊", layout="wide")

# Custom CSS for better appearance
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border: none;
        border-radius: 4px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stDownloadButton>button {
        background-color: #008CBA;
        color: white;
    }
    .stFileUploader>div>div>div>button {
        background-color: #f39c12;
        color: white;
    }
    .title {
        color: #2c3e50;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.title("BE Computer Engineering Marks Parser")
st.markdown("Upload your PDF marksheet to convert it to CSV format")

class TheoryMarks:
    def __init__(self):
        self.marks = "NA"

    def set_marks(self, marks: str):
        if marks == "FF":
            self.marks = "F"
        elif "$" in marks:
            self.marks = marks.split("$")[0]
        else:
            if "/" in marks:
                self.marks = marks.split("/")[0]
                if self.marks[0] == "0":
                    self.marks = self.marks[1:]  # remove the first 0
            else:
                self.marks = marks

    def print(self) -> int:
        return self.marks


class LabMarks:
    def __init__(
        self,
        TW_marks: str = "---",
        PR_marks: str = "---",
        OR_marks: str = "---",
        Total_marks: str = "---",
    ):
        self.PR_marks = PR_marks  # format scored-marks/total-marks
        self.OR_marks = OR_marks
        self.TW_marks = TW_marks
        self.Total_marks = Total_marks

    def set_data(self, data: list[str]):
        self.TW_marks = data[3].strip()
        self.PR_marks = data[4].strip()
        self.OR_marks = data[5].strip()
        self.Total_marks = data[6].split("   ")[0].strip()

    def ret_data(self) -> list[str]:
        marks_list = []
        if self.TW_marks != "---" and "AB" not in self.TW_marks and "$" not in self.TW_marks:
            if int(self.TW_marks.split("/")[1]) == 50:
                self.TW_marks = self.TW_marks.split("/")[0]
                marks_list.append(int(self.TW_marks)*2)
            elif int(self.TW_marks.split("/")[1]) == 25:
                self.TW_marks = self.TW_marks.split("/")[0]
                marks_list.append(int(self.TW_marks)*4)
            else:
                marks_list.append(int(self.TW_marks.split("/")[0]))
        elif "AB" in self.TW_marks:
            marks_list.append("AB")
        elif "$" in self.TW_marks:
            marks_list.append(int(self.TW_marks.split("$")[0]))
        else:
            marks_list.append("NA")
        
        if self.PR_marks != "---" and "AB" not in self.PR_marks and "$" not in self.PR_marks:
            if int(self.PR_marks.split("/")[1]) == 50:
                self.PR_marks = self.PR_marks.split("/")[0]
                marks_list.append(int(self.PR_marks)*2)
            elif int(self.PR_marks.split("/")[1]) == 25:
                self.PR_marks = self.PR_marks.split("/")[0]
                marks_list.append(int(self.PR_marks)*4)
        elif "AB" in self.PR_marks:
            marks_list.append("AB")
        elif "$" in self.PR_marks:
            marks_list.append(int(self.PR_marks.split("$")[0]))
        else:
            marks_list.append("NA")
        
        if self.OR_marks != "---" and "AB" not in self.OR_marks and "$" not in self.OR_marks:
            if int(self.OR_marks.split("/")[1]) == 50:
                self.OR_marks = self.OR_marks.split("/")[0]
                marks_list.append(int(self.OR_marks)*2)
            elif int(self.OR_marks.split("/")[1]) == 25:
                self.OR_marks = self.OR_marks.split("/")[0]
                marks_list.append(int(self.OR_marks)*4)
        elif "AB" in self.OR_marks:
            marks_list.append("AB")
        elif "$" in self.OR_marks:
            marks_list.append(int(self.OR_marks.split("$")[0]))
        else:
            marks_list.append("NA")
        marks_list.append(self.Total_marks)

        return marks_list


class Student:
    def __init__(self):
        self.full_name = ""
        self.seat_no = ""
        self.theory_marks_sub1 = TheoryMarks()
        self.theory_marks_sub2 = TheoryMarks()
        self.theory_marks_sub3 = TheoryMarks()
        self.theory_marks_sub4 = TheoryMarks()
        self.theory_marks_sub5 = TheoryMarks()
        self.theory_marks_sub6 = TheoryMarks()
        self.theory_marks_sub7 = TheoryMarks()
        self.theory_marks_sub8 = TheoryMarks()
        self.theory_marks_sub9 = TheoryMarks()
        self.theory_marks_sub10 = TheoryMarks()
        self.theory_marks_sub11 = TheoryMarks()
        self.lab_marks_sub1 = LabMarks()
        self.lab_marks_sub2 = LabMarks()
        self.lab_marks_sub3 = LabMarks()
        self.SGPA = 0
        self.Credits = 0

    def tolist(self) -> list[str, int]:
        lab1 = self.lab_marks_sub1.ret_data()
        lab2 = self.lab_marks_sub2.ret_data()
        lab3 = self.lab_marks_sub3.ret_data()
        return [
            self.seat_no,
            self.full_name,
            self.theory_marks_sub1.print(),
            self.theory_marks_sub2.print(),
            self.theory_marks_sub3.print(),
            self.theory_marks_sub4.print(),
            self.theory_marks_sub5.print(),
            self.theory_marks_sub6.print(),
            self.theory_marks_sub7.print(),
            self.theory_marks_sub8.print(),
            self.theory_marks_sub9.print(),
            self.theory_marks_sub10.print(),
            self.theory_marks_sub11.print(),
            lab1[0],
            lab1[1],
            lab1[2],
            lab2[0],
            lab2[1],
            lab2[2],
            lab3[0],
            lab3[1],
            lab3[2],
            self.SGPA,
            self.Credits
        ]

    def clear(self):
        self.full_name = ""
        self.seat_no = ""
        self.theory_marks_sub1 = TheoryMarks()
        self.theory_marks_sub2 = TheoryMarks()
        self.theory_marks_sub3 = TheoryMarks()
        self.theory_marks_sub4 = TheoryMarks()
        self.theory_marks_sub5 = TheoryMarks()
        self.theory_marks_sub6 = TheoryMarks()
        self.theory_marks_sub7 = TheoryMarks()
        self.theory_marks_sub8 = TheoryMarks()
        self.theory_marks_sub9 = TheoryMarks()
        self.theory_marks_sub10 = TheoryMarks()
        self.theory_marks_sub11 = TheoryMarks()
        self.lab_marks_sub1 = LabMarks()
        self.lab_marks_sub2 = LabMarks()
        self.lab_marks_sub3 = LabMarks()
        self.SGPA = 0


def parse_pdf(input_pdf_path):
    # Create a temporary file for CSV output
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
        output_csv_path = tmp_file.name
    
    # Initialize CSV writer
    with open(output_csv_path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([
            "Seat No",
            "Name",
            "DESIGN & ANALYSIS OF ALGO",
            "MACHINE LEARNING",
            "BLOCKCHAIN TECHNOLOGY",
            "PERVASIVE COMPUTING",
            "MULTIMEDIA TECHNIQUES",
            "CYBER SEC & DIGITAL FORENSICS",
            "OBJ. ORIENTED MODL. & DESIGN",
            "INFORMATION RETRIEVAL",
            "GPU PROG. & ARCHITECTURE",
            "MOBILE COMPUTING",
            "SOFTWARE TESTING & QUALITY ASSURANCE",
            "LABORATORY",
            "PRACTICE",
            "III",
            "LABORATORY",
            "PRACTICE",
            "IV",
            "PROJECT",
            "STAGE",
            "I",
            "SGPA",
            "Credits"
        ])
        csv_writer.writerow([
            " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
            "TW", "PR", "OR", "TW", "PR", "OR", "TW", "PR", "OR",
        ])

        # Initialize parsing variables
        counter = -1
        student = Student()
        object_counter = 0

        def ordered_parse(parse_line: str):
            nonlocal counter, student, object_counter
            
            if (
                "CONFIDENTIAL" in parse_line
                or "COURSE" in parse_line
                or "SEM" in parse_line
                or "410301" in parse_line
                or "410501" in parse_line
                or "410401" in parse_line
                or "410402" in parse_line
                or "410249" in parse_line
                or "411701" in parse_line
                or "410250" in parse_line
                or "410251" in parse_line
                or "410252" in parse_line
                or "410253" in parse_line
                or "410254" in parse_line
                or "410255" in parse_line
                or "410256" in parse_line
                or "410257" in parse_line
                or "FE SGPA" in parse_line
                or "SE SGPA" in parse_line
                or "TOTAL GRADE" in parse_line
            ):
                return

            order_dict = {
                -1: "Seat and Name",
                0: student.theory_marks_sub1,
                1: student.theory_marks_sub2,
                2: student.theory_marks_sub3,
                3: student.theory_marks_sub4,
                4: student.theory_marks_sub5,
                5: student.theory_marks_sub6,
                6: student.theory_marks_sub7,
                7: student.theory_marks_sub8,
                8: student.theory_marks_sub9,
                9: student.theory_marks_sub10,
                10: student.theory_marks_sub11,
                11: student.lab_marks_sub1,
                12: student.lab_marks_sub2,
                13: student.lab_marks_sub3,
            }

            if counter == -1:
                student.full_name = parse_line.split(":")[2].split("    ")[0]
                seat_no = parse_line.split(":")[1].split(" ")[1]
                if seat_no.endswith("NAME"):
                    seat_no = seat_no[:-4]
                student.seat_no = seat_no
                counter += 1
                return

            if counter < 11 and counter > -1:
                if "*" not in parse_line:
                    index = parse_line.find("/")
                    index -= 3
                    con_str = parse_line[index:]
                    total_marks = list(map("".join, zip(*[iter(con_str)] * 9)))[2].split("   ")[0]
                else:
                    con_str = parse_line.split("*")[1]
                    total_marks = list(map("".join, zip(*[iter(con_str)] * 9)))[2].split("   ")[0]
                
                if counter == 3:
                    if "410244A" in parse_line:
                        order_dict[counter].set_marks(total_marks.strip())
                    elif "410244B" in parse_line:
                        order_dict[counter+1].set_marks(total_marks.strip())
                    elif "410244C" in parse_line:
                        order_dict[counter+2].set_marks(total_marks.strip())
                    elif "410244D" in parse_line:
                        order_dict[counter+3].set_marks(total_marks.strip())
                    counter = 7
                elif counter == 7:
                    if "410245A" in parse_line:
                        order_dict[counter].set_marks(total_marks.strip())
                    elif "410245B" in parse_line:
                        order_dict[counter+1].set_marks(total_marks.strip())
                    elif "410245C" in parse_line:
                        order_dict[counter+2].set_marks(total_marks.strip())
                    elif "410245D" in parse_line:
                        order_dict[counter+3].set_marks(total_marks.strip())
                    counter = 11
                else:
                    order_dict[counter].set_marks(total_marks.strip())
                    counter += 1
            elif "SGPA" in parse_line:
                student.SGPA = parse_line.split(":")[1].split(",")[0]
                student.Credits = parse_line.split(":")[-1].strip()
                csv_writer.writerow(student.tolist())
                counter = -1
                object_counter += 1
                student.clear()
            else:
                if "*" not in parse_line:
                    index = parse_line.find("---")
                    con_str = "   " + parse_line[index:]
                else:
                    con_str = parse_line.split("*")[1]
                data = list(map("".join, zip(*[iter(con_str)] * 9)))
                order_dict[counter].set_data(data)
                counter += 1

        # Parse the PDF
        for page_layout in extract_pages(input_pdf_path):
            for element in page_layout:
                if isinstance(element, (LTTextBoxHorizontal)):
                    if "PUNE" in element.get_text():
                        continue
                    else:
                        for text_line in element:
                            ordered_parse(text_line.get_text())

    return output_csv_path, object_counter


# Streamlit UI
uploaded_file = st.file_uploader("Upload PDF Marksheet", type="pdf")

if uploaded_file is not None:
    with st.spinner("Parsing PDF..."):
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
            tmp_pdf.write(uploaded_file.getvalue())
            tmp_pdf_path = tmp_pdf.name
        
        # Parse the PDF
        csv_path, num_students = parse_pdf(tmp_pdf_path)
        
        # Clean up temporary PDF file
        os.unlink(tmp_pdf_path)
        
        # Display success message
        st.success(f"Successfully parsed {num_students} student records!")
        
        # Show preview of the CSV
        df = pd.read_csv(csv_path)
        st.subheader("Preview of Parsed Data")
        st.dataframe(df.head())
        
        # Download button
        with open(csv_path, "rb") as f:
            st.download_button(
                label="Download CSV",
                data=f,
                file_name="parsed_marks.csv",
                mime="text/csv"
            )
        
        # Clean up temporary CSV file
        os.unlink(csv_path)