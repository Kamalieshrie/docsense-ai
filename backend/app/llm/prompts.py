# ============================================================
# prompts.py — 8 document-type-specific prompts
# Each document type gets its OWN targeted prompt
# ============================================================

CLASSIFY_PROMPT = """
Look at this document carefully.
What type of document is this? Choose EXACTLY ONE from:
bank_statement | invoice | receipt | medical_bill | certificate |
id_proof | cheque | resume | property_doc | contract |
salary_slip | utility_bill | insurance | admission_letter |
tax_document | vehicle_rc | rental_agreement | unknown

Return ONLY the category word. Nothing else.
"""

PROMPTS = {

"bank_statement": """
You are a precise bank statement extractor.
OCR Text from document:
{ocr_text}

Extract ALL of the following.
Only use values LITERALLY visible in the document.
NEVER invent, calculate or assume any value.

Return valid JSON:
{{
  "document_type": "bank_statement",
  "bank_name": "",
  "account_holder": "",
  "account_number": "",
  "statement_period": {{"from": "", "to": ""}},
  "opening_balance": "",
  "closing_balance": "",
  "total_credits": "",
  "total_debits": "",
  "total_interest": "",
  "average_balance": "",
  "service_charges": "",
  "transactions": [
    {{"date": "", "description": "", "debit": "", "credit": "", "balance": ""}}
  ],
  "checks_paid": [
    {{"check_number": "", "date": "", "amount": ""}}
  ]
}}
""",

"invoice": """
You are a precise invoice extractor.
OCR Text:
{ocr_text}

Extract ALL visible fields. Return JSON:
{{
  "document_type": "invoice",
  "invoice_number": "",
  "invoice_date": "",
  "due_date": "",
  "vendor": {{"name": "", "address": "", "phone": "", "email": ""}},
  "customer": {{"name": "", "address": "", "phone": "", "email": ""}},
  "line_items": [
    {{"description": "", "quantity": "", "unit_price": "", "total": ""}}
  ],
  "subtotal": "",
  "tax": "",
  "discount": "",
  "grand_total": "",
  "payment_terms": "",
  "notes": ""
}}
""",

"receipt": """
You are a precise receipt extractor.
OCR Text:
{ocr_text}

Return JSON:
{{
  "document_type": "receipt",
  "store_name": "",
  "store_address": "",
  "receipt_number": "",
  "date": "",
  "time": "",
  "items": [
    {{"name": "", "quantity": "", "price": ""}}
  ],
  "subtotal": "",
  "tax": "",
  "discount": "",
  "total": "",
  "payment_method": "",
  "cashier": ""
}}
""",

"medical_bill": """
You are a precise medical bill extractor.
OCR Text:
{ocr_text}

Return JSON:
{{
  "document_type": "medical_bill",
  "hospital_name": "",
  "patient_name": "",
  "patient_id": "",
  "doctor_name": "",
  "date": "",
  "services": [
    {{"description": "", "quantity": "", "amount": ""}}
  ],
  "medicines": [
    {{"name": "", "dosage": "", "quantity": "", "amount": ""}}
  ],
  "subtotal": "",
  "insurance_covered": "",
  "amount_due": ""
}}
""",

"certificate": """
You are a precise certificate and marksheet extractor.
OCR Text:
{ocr_text}

Return JSON:
{{
  "document_type": "certificate",
  "certificate_type": "",
  "student_name": "",
  "register_number": "",
  "institution": "",
  "board_university": "",
  "year": "",
  "subjects": [
    {{"subject": "", "marks_obtained": "", "max_marks": "", "grade": ""}}
  ],
  "total_marks": "",
  "percentage": "",
  "cgpa": "",
  "result": ""
}}
""",

"id_proof": """
You are a precise ID document extractor.
OCR Text:
{ocr_text}

Return JSON:
{{
  "document_type": "id_proof",
  "id_type": "",
  "full_name": "",
  "date_of_birth": "",
  "id_number": "",
  "address": "",
  "issue_date": "",
  "expiry_date": "",
  "issuing_authority": ""
}}
""",

"cheque": """
You are a precise bank cheque extractor.
OCR Text:
{ocr_text}

Return JSON:
{{
  "document_type": "cheque",
  "bank_name": "",
  "branch": "",
  "cheque_number": "",
  "date": "",
  "pay_to": "",
  "amount_in_numbers": "",
  "amount_in_words": "",
  "account_number": "",
  "ifsc_code": "",
  "micr_code": ""
}}
""",

"resume": """
You are a precise resume extractor.
OCR Text:
{ocr_text}

Return JSON:
{{
  "document_type": "resume",
  "full_name": "",
  "email": "",
  "phone": "",
  "location": "",
  "linkedin": "",
  "skills": [],
  "education": [
    {{"degree": "", "institution": "", "year": "", "score": ""}}
  ],
  "experience": [
    {{"role": "", "company": "", "duration": "", "description": ""}}
  ],
  "certifications": [],
  "projects": [
    {{"name": "", "description": "", "tech_stack": ""}}
  ]
}}
""",

"property_doc": """
You are a precise property document extractor.
This is an Indian legal property document — stamp paper, sale deed, power of attorney, or agreement.
OCR Text:
{ocr_text}

Extract ALL visible fields. Return JSON:
{{
  "document_type": "property_doc",
  "document_title": "",
  "document_number": "",
  "execution_date": "",
  "stamp_value": "",
  "stamp_paper_number": "",
  "registration_number": "",
  "vendor": {{
    "name": "",
    "father_name": "",
    "age": "",
    "occupation": "",
    "address": "",
    "aadhar_number": ""
  }},
  "vendees": [
    {{
      "name": "",
      "father_name": "",
      "age": "",
      "occupation": "",
      "address": "",
      "aadhar_number": ""
    }}
  ],
  "property_details": {{
    "survey_number": "",
    "village": "",
    "mandal": "",
    "district": "",
    "state": "",
    "area": "",
    "boundaries": ""
  }},
  "consideration_amount": "",
  "stamp_vendor": "",
  "witness_names": [],
  "sub_registrar_office": ""
}}
""",

"contract": """
You are a precise legal contract extractor.
OCR Text:
{ocr_text}

Return JSON:
{{
  "document_type": "contract",
  "contract_title": "",
  "contract_date": "",
  "party_1": {{
    "name": "",
    "address": "",
    "role": ""
  }},
  "party_2": {{
    "name": "",
    "address": "",
    "role": ""
  }},
  "effective_date": "",
  "expiry_date": "",
  "key_terms": [],
  "payment_terms": "",
  "governing_law": "",
  "signatures": []
}}
""",

"salary_slip": """
You are a precise salary slip extractor.
OCR Text:
{ocr_text}

Return JSON:
{{
  "document_type": "salary_slip",
  "company_name": "",
  "employee_name": "",
  "employee_id": "",
  "designation": "",
  "department": "",
  "month_year": "",
  "bank_account": "",
  "pan_number": "",
  "earnings": [
    {{"component": "", "amount": ""}}
  ],
  "deductions": [
    {{"component": "", "amount": ""}}
  ],
  "gross_salary": "",
  "total_deductions": "",
  "net_salary": "",
  "pf_number": "",
  "uan_number": ""
}}
""",

"utility_bill": """
You are a precise utility bill extractor.
OCR Text:
{ocr_text}

Return JSON:
{{
  "document_type": "utility_bill",
  "bill_type": "",
  "service_provider": "",
  "consumer_name": "",
  "consumer_number": "",
  "address": "",
  "bill_number": "",
  "bill_date": "",
  "due_date": "",
  "billing_period": {{"from": "", "to": ""}},
  "units_consumed": "",
  "previous_reading": "",
  "current_reading": "",
  "amount_due": "",
  "late_fee": "",
  "total_amount": ""
}}
""",

"insurance": """
You are a precise insurance document extractor.
OCR Text:
{ocr_text}

Return JSON:
{{
  "document_type": "insurance",
  "insurance_type": "",
  "policy_number": "",
  "policy_holder": "",
  "date_of_birth": "",
  "nominee": "",
  "insurer_name": "",
  "sum_insured": "",
  "premium_amount": "",
  "premium_frequency": "",
  "policy_start_date": "",
  "policy_end_date": "",
  "coverage_details": [],
  "agent_name": "",
  "agent_code": ""
}}
""",

"admission_letter": """
You are a precise admission letter extractor.
OCR Text:
{ocr_text}

Return JSON:
{{
  "document_type": "admission_letter",
  "institution_name": "",
  "student_name": "",
  "application_number": "",
  "course_name": "",
  "specialization": "",
  "academic_year": "",
  "admission_date": "",
  "fee_amount": "",
  "fee_due_date": "",
  "hostel_allotted": "",
  "reporting_date": "",
  "conditions": []
}}
""",

"tax_document": """
You are a precise income tax document extractor.
OCR Text:
{ocr_text}

Return JSON:
{{
  "document_type": "tax_document",
  "form_type": "",
  "assessment_year": "",
  "taxpayer_name": "",
  "pan_number": "",
  "employer_name": "",
  "employer_tan": "",
  "gross_salary": "",
  "exemptions": "",
  "taxable_income": "",
  "tax_deducted": "",
  "surcharge": "",
  "total_tax_paid": "",
  "acknowledgement_number": ""
}}
""",

"vehicle_rc": """
You are a precise vehicle registration document extractor.
OCR Text:
{ocr_text}

Return JSON:
{{
  "document_type": "vehicle_rc",
  "registration_number": "",
  "owner_name": "",
  "owner_address": "",
  "vehicle_class": "",
  "maker_model": "",
  "body_type": "",
  "fuel_type": "",
  "engine_number": "",
  "chassis_number": "",
  "color": "",
  "registration_date": "",
  "fitness_valid_upto": "",
  "insurance_valid_upto": "",
  "rto_office": ""
}}
""",

"rental_agreement": """
You are a precise rental agreement extractor.
OCR Text:
{ocr_text}

Return JSON:
{{
  "document_type": "rental_agreement",
  "agreement_date": "",
  "landlord": {{
    "name": "",
    "address": "",
    "phone": "",
    "aadhar": ""
  }},
  "tenant": {{
    "name": "",
    "address": "",
    "phone": "",
    "aadhar": ""
  }},
  "property_address": "",
  "monthly_rent": "",
  "security_deposit": "",
  "lease_start_date": "",
  "lease_end_date": "",
  "lock_in_period": "",
  "notice_period": "",
  "maintenance_charges": "",
  "witnesses": []
}}
""",

"unknown": """
You are a document extractor.
OCR Text:
{ocr_text}

Read every piece of visible information and return it as JSON.
Use descriptive keys based on what you actually see.
NEVER invent information. Only extract what is literally present.
Return JSON with all visible fields.
""",
}