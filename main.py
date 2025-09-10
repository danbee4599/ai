from scrape import (
    start,
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_content,
)
from cut import cut

companies_text = """Regeneron Pharmaceuticals, Inc.
Elevance Health, Inc.
Vertex Pharmaceuticals Incorporated
Boston Scientific Corporation
Medtronic plc
EssilorLuxottica Société anonyme
CSL Limited
Bristol-Myers Squibb Company
The Cigna Group
HCA Healthcare, Inc.
Gilead Sciences, Inc.
Zoetis Inc.
GSK plc
Merck KGaA
CVS Health Corporation
Daiichi Sankyo Company, Limited
McKesson Corporation
Chugai Pharmaceutical Co., Ltd.
Becton, Dickinson and Company
Siemens Healthineers AG
Sun Pharmaceutical Industries Limited
Samsung Biologics Co.,Ltd.
HOYA Corporation
Cencora, Inc.
Alcon Inc.
Lonza Group AG
Shenzhen Mindray Bio-Medical Electronics Co., Ltd.
Takeda Pharmaceutical Company Limited
Haleon plc
IQVIA Holdings Inc.
Humana Inc.
Centene Corporation
Agilent Technologies, Inc.
IDEXX Laboratories, Inc."""
companies_list = companies_text.splitlines()

driver = start()

for c in companies_list:
    dom_content = scrape_website(driver, c)
    body_content = extract_body_content(dom_content)
    cleaned_content = clean_body_content(body_content)
    final_text = cut(cleaned_content)

    file_name = c.replace(" ", "_")

    with open(f"{file_name}.txt", "w", encoding="utf-8") as f:
        f.write(final_text)



