from weasyprint import HTML, CSS
import json
import tags

# sample_questions = [
#     {
#         "question_text": "25 + 18 =",
#         "options": ["12", "2", "43", "22"],
#         "correct_option": "3",
#         "difficulty_level": "2",
#         "skill_code": "2A2C"
#     },
#     {
#         "question_text": "25 - 12 =",
#         "options": ["13", "2", "43", "22"],
#         "correct_option": "1",
#         "difficulty_level": "2",
#         "skill_code": "2S2"
#     },
#     {
#         "question_text": "25 - 18 =",
#         "options": ["12", "2", "43", "7"],
#         "correct_option": "4",
#         "difficulty_level": "2",
#         "skill_code": "2S2B"
#     },
#     {
#         "question_text": "25 - 25 =",
#         "options": ["12", "2", "0", "22"],
#         "correct_option": "3",
#         "difficulty_level": "3",
#         "skill_code": "2S2"
#     },
#     {
#         "question_text": "2 + 2 =",
#         "options": ["0", "22", "4", "5"],
#         "correct_option": "3",
#         "difficulty_level": "1",
#         "skill_code": "1A"
#     },
#     {
#         "question_text": "9 - 5 =",
#         "options": ["4", "14", "5", "2"],
#         "correct_option": "1",
#         "difficulty_level": "1",
#         "skill_code": "1S"
#     },
#     {
#         "question_text": "3 × 4 =",
#         "options": ["34", "3", "7", "12"],
#         "correct_option": "4",
#         "difficulty_level": "1",
#         "skill_code": "T5"
#     },
#     {
#         "question_text": "9 + 4 =",
#         "options": ["5", "12", "13", "15"],
#         "correct_option": "3",
#         "difficulty_level": "2",
#         "skill_code": "1AC"
#     },
#     {
#         "question_text": "17 + 9 =",
#         "options": ["8", "79", "43", "26"],
#         "correct_option": "4",
#         "difficulty_level": "2",
#         "skill_code": "2A1C"
#     },
#     {
#         "question_text": "32 - 19 =",
#         "options": ["13", "23", "42", "18"],
#         "correct_option": "1",
#         "difficulty_level": "3",
#         "skill_code": "2S2B"
#     },
#     {
#         "question_text": "999 - 888 =",
#         "options": ["110", "111", "191", "1807"],
#         "correct_option": "2",
#         "difficulty_level": "2",
#         "skill_code": "3S"
#     },
#     {
#         "question_text": "14 - 9 =",
#         "options": ["12", "2", "5", "22"],
#         "correct_option": "3",
#         "difficulty_level": "3",
#         "skill_code": "2S1B"
#     },
#     {
#         "question_text": "31 × 12 =",
#         "options": ["372", "32", "43", "651"],
#         "correct_option": "1",
#         "difficulty_level": "5",
#         "skill_code": "2M2"
#     },
#     {
#         "question_text": "81 ÷ 3 =",
#         "options": ["9", "12", "43", "27"],
#         "correct_option": "4",
#         "difficulty_level": "5",
#         "skill_code": "2D1"
#     },
#     {
#         "question_text": "123 ÷ 3 =",
#         "options": ["126", "4", "41", "9"],
#         "correct_option": "3",
#         "difficulty_level": "5",
#         "skill_code": "3D1"
#     },
#     {
#         "question_text": "69 × 69 =",
#         "options": ["1212", "138", "4761", "1981"],
#         "correct_option": "3",
#         "difficulty_level": "5",
#         "skill_code": "2M2C"
#     },
#     {
#         "question_text": "70 ÷ 4 =",
#         "options": ["17", "21", "74", "18"],
#         "correct_option": "1",
#         "difficulty_level": "6",
#         "skill_code": "2D1R"
#     },
#     {
#         "question_text": "123 ÷ 5 =",
#         "options": ["314", "11", "24", "42"],
#         "correct_option": "3",
#         "difficulty_level": "6",
#         "skill_code": "3D1R"
#     },
#     {
#         "question_text": "479 × 34 =",
#         "options": ["16,286", "16,765", "15,328", "20,597"],
#         "correct_option": "1",
#         "difficulty_level": "6",
#         "skill_code": "3M2C"
#     },
#     {
#         "question_text": "601 ÷ 5 =",
#         "options": ["210", "120", "20", "81"],
#         "correct_option": "2",
#         "difficulty_level": "6",
#         "skill_code": "3D1Z"
#     }
# ]

# opens a json worksheet file
def open_worksheet(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # ansKey = data[0].answerKey
    questions = data[1]

    return questions

# from a worksheet ID (check database), get the tags to be inserted
def getTagNumbers(id):
    idTags = tags.encode_worksheet_id(id)
    idTags.insert(0, tags.ORIENTATION_ID)

    return idTags

# only for corner tags (36h11)
def generate_tags_html(tags):
    tag_urls = [f"tags/36h11/tag36_11_{str(id).zfill(5)}.svg" for id in tags]
    print(f"tag urls: {tag_urls}")
    tags_html = ""

    print(f"Adding tags {tag_urls}")
    tags_html += f'<div class="marker top-left" style="background-image: url({tag_urls[0]})"></div>\n'
    tags_html += f'<div class="marker top-right" style="background-image: url({tag_urls[1]})""></div>\n'
    tags_html += f'<div class="marker bottom-left" style="background-image: url({tag_urls[2]})"></div>\n'
    tags_html += f'<div class="marker bottom-right" style="background-image: url({tag_urls[3]})"></div>\n'

    return tags_html

def generate_question_box(question, q_no):
    option_html = ""

    option_html += "<td class='question_td'>\n <div class='question'>\n"
    option_html += f"<p>{q_no}. {question['question_text']}</p>"
    option_html += "<table class='options-table'>\n <tr>"
    option_html += f"<td><div class='circle'></div>A. {question['options'][0]}</td>"
    option_html += f"<td><div class='circle'></div>B. {question['options'][1]}</td>"
    option_html += f"<td><div class='circle'></div>C. {question['options'][2]}</td>"
    option_html += f"<td><div class='circle'></div>D. {question['options'][3]}</td>"
    option_html += "</tr>\n </table>"
    option_html += "</div>\n </td>"

    return option_html

def generate_questions_html(questions):
    rows_html = ""
    for i in range(0, len(questions), 2):
        q1 = questions[i]
        q2 = questions[i+1] if i+1 < len(questions) else None
        rows_html += "<tr>\n"
        # add one marker per row
        rows_html += "<td class='row-marker'>\n"

        # tag url for 25h9
        tag_url = f"tags/25h9/tag25_09_{str((i // 2) + 1).zfill(5)}.svg"

        # tag url for 36h11 tags number 10-20
        # tag_url = f"tags/36h11/tag36_11_{str((i // 2) + 10).zfill(5)}.svg"

        print(f"Adding {tag_url}")
        rows_html += f"<div class='marker' style='background-image: url({tag_url})'></div>\n"
        rows_html += "</td>\n"
        rows_html += f"{generate_question_box(q1, i+1)}\n"
        rows_html += f"{generate_question_box(q2, i+2) if q2 else ''}\n"
        rows_html += "</tr>\n"
    
    return rows_html

if __name__ == "__main__":

    worksheet_id = 2

    with open("template.html", "r", encoding="utf-8") as f:
        template_html = f.read()

    questions = open_worksheet('marathi.json')
    questions_html = generate_questions_html(questions)
    tags_html = generate_tags_html(getTagNumbers(worksheet_id))
    final_html = template_html.replace("{{tags_html}}", tags_html).replace("{{questions}}", questions_html)

    HTML(string=final_html, base_url=".").write_pdf("output.pdf")