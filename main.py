import json
import sys
import io
from datetime import datetime
import psycopg2

# แสดงเวอร์ชัน psycopg2
print(f"psycopg2 version: {psycopg2.__version__}")

# ตั้งค่า stdout และ stderr เป็น UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# การตั้งค่าการเชื่อมต่อฐานข้อมูล
DB_CONFIG = {
    'host': '127.0.0.1',
    'database': 'eopen',
    'user': 'postgres',
    'password': 'ramil999',  # เปลี่ยนเป็นรหัสผ่าน PostgreSQL ของคุณ
    'port': '5432'
}

# Title mapping for eopen_sba and eopen_stt
TITLE_MAPPING = {
    'mr': 'นาย',
    'miss': 'นางสาว',
    'ms': 'นาง',
    'mrs': 'นาง',
    'นาย': 'นาย',
    'นาง': 'นาง',
    'นางสาว': 'นางสาว'
}

# English title mapping
ETITLE_MAPPING = {
    'mr': 'MR',
    'miss': 'MISS',
    'ms': 'MRS',
    'mrs': 'MRS'
}

def connect_db():
    """Create a connection to PostgreSQL database"""
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        connection.set_client_encoding('UTF8')
        print("Successfully connected to PostgreSQL database")
        print(f"Client encoding set to: {connection.encoding}")
        return connection
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def read_json_file(filename):
    """Read JSON file and return data"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(f"Successfully loaded JSON data from {filename}")
        # ไม่พิมพ์ JSON เพื่อป้องกัน UnicodeEncodeError
        # หากต้องการดีบัก สามารถบันทึก JSON ลงไฟล์แทน
        # with open('debug_json_output.json', 'w', encoding='utf-8') as f:
        #     json.dump(data, f, ensure_ascii=False, indent=2)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: File '{filename}' contains invalid JSON.")
        return None
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

def safe_trim(value, max_length):
    """Trim string to not exceed max_length, return empty string if None"""
    if value is None:
        return ''
    value_str = str(value).strip()
    return value_str[:max_length] if value_str else ''

def format_date(date_string):
    """Convert various date formats to YYYYMMDD or return None if invalid"""
    if not date_string:
        return None
    formats = [
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%Y%m%d"
    ]
    for fmt in formats:
        try:
            date_obj = datetime.strptime(date_string, fmt)
            if date_obj.year > 2500:
                date_obj = date_obj.replace(year=date_obj.year - 543)
            return date_obj.strftime('%Y%m%d')
        except ValueError:
            continue
    return None

def format_datetime(dt):
    """Convert datetime object to PostgreSQL-compatible string"""
    if dt is None:
        return None
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def transform_title(title):
    """Transform title to Thai format (นาย, นาง, นางสาว)"""
    if not title:
        return ''
    title_lower = title.lower().strip()
    return TITLE_MAPPING.get(title_lower, '')

def transform_etitle(title):
    """Transform title to English format (MR, MISS, MRS)"""
    if not title:
        return ''
    title_lower = title.lower().strip()
    return ETITLE_MAPPING.get(title_lower, '')

def check_values_for_percent(values):
    """Check if any string value contains a '%' character"""
    for i, v in enumerate(values):
        if isinstance(v, str) and '%' in v:
            print(f"[DEBUG] Value at index {i} contains '%': {v}")
            return True
    return False

def insert_sba_data(json_data, connection):
    """Insert data into eopen_sba table using parameterized query"""
    print("[DEBUG SBA] Starting insert_sba_data function")
    if not json_data or not connection:
        print("No JSON data or database connection")
        return False
    print("[DEBUG SBA] JSON data and connection are valid")

    # Extract application data
    print("[DEBUG SBA] Extracting app_data")
    app_data = json_data.get('appId', {})
    app_id = app_data.get('applicationId')
    if app_id is None:
        print("Error: app_id is required but missing in JSON")
        return False
    app_id = int(app_id)
    print(f"[DEBUG SBA] app_id: {app_id}")

    print("[DEBUG SBA] Extracting data")
    data = app_data.get('data', {})

    # Validate required fields
    print("[DEBUG SBA] Validating required fields")
    required_fields = [
        'appId.applicationId',
        'appId.data.thFirstName',
        'appId.data.thLastName',
        'appId.data.cardNumber',
        'appId.data.birthDate.formatted'
    ]
    for field in required_fields:
        keys = field.split('.')
        value = json_data
        for key in keys:
            value = value.get(key, {})
        if not value:
            print(f"Missing required field: {field}")
            return False
    print("[DEBUG SBA] All required fields are present")

    try:
        print("[DEBUG SBA] Creating cursor")
        cursor = connection.cursor()

        # Extract addresses
        print("[DEBUG SBA] Extracting addresses")
        residence = {
            'no': data.get('residence', {}).get('no', ''),
            'moo': data.get('residence', {}).get('moo', ''),
            'village': data.get('residence', {}).get('village', ''),
            'building': data.get('residence', {}).get('building', ''),
            'floor': data.get('residence', {}).get('floor', ''),
            'soi': data.get('residence', {}).get('soi', ''),
            'road': data.get('residence', {}).get('road', ''),
            'sub_district': data.get('residence', {}).get('subDistrict', ''),
            'district': data.get('residence', {}).get('district', ''),
            'province': data.get('residence', {}).get('province', ''),
            'country': data.get('residence', {}).get('country', 'TH'),
            'postal_code': data.get('residence', {}).get('postalCode', '')
        }
        mailing = {
            'no': data.get('mailing', {}).get('no', ''),
            'moo': data.get('mailing', {}).get('moo', ''),
            'village': data.get('mailing', {}).get('village', ''),
            'building': data.get('mailing', {}).get('building', ''),
            'floor': data.get('mailing', {}).get('floor', ''),
            'soi': data.get('mailing', {}).get('soi', ''),
            'road': data.get('mailing', {}).get('road', ''),
            'sub_district': data.get('mailing', {}).get('subDistrict', ''),
            'district': data.get('mailing', {}).get('district', ''),
            'province': data.get('mailing', {}).get('province', ''),
            'country': data.get('mailing', {}).get('country', 'TH'),
            'postal_code': data.get('mailing', {}).get('postalCode', '')
        }
        work = {
            'no': data.get('work', {}).get('no', ''),
            'moo': data.get('work', {}).get('moo', ''),
            'village': data.get('work', {}).get('village', ''),
            'building': data.get('work', {}).get('building', ''),
            'floor': data.get('work', {}).get('floor', ''),
            'soi': data.get('work', {}).get('soi', ''),
            'road': data.get('work', {}).get('road', ''),
            'sub_district': data.get('work', {}).get('subDistrict', ''),
            'district': data.get('work', {}).get('district', ''),
            'province': data.get('work', {}).get('province', ''),
            'country': data.get('work', {}).get('country', 'TH'),
            'postal_code': data.get('work', {}).get('postalCode', '')
        }
        print("[DEBUG SBA] Addresses extracted")

        # Extract bank account info
        print("[DEBUG SBA] Extracting bank account info")
        redemption_accounts = data.get('otherAccountInfo', {}).get('redemptionBankAccounts', [{}])[0] if data.get(
            'otherAccountInfo', {}).get('redemptionBankAccounts') else {}
        ddr_bank = data.get('otherAccountInfo', {}).get('ddrBank', {}).get('key', '') if data.get('otherAccountInfo',
                                                                                                  {}) else ''
        ddr_bank_account_no = app_data.get('ddrBankAccountNo', '')
        print("[DEBUG SBA] Bank account info extracted")

        # Extract personal info
        print("[DEBUG SBA] Extracting personal info")
        title = transform_title(data.get('title', {}).get('key', '') if isinstance(data.get('title'), dict) else '')
        etitle = transform_etitle(data.get('title', {}).get('key', '') if isinstance(data.get('title'), dict) else '')
        th_first_name = safe_trim(data.get('thFirstName', ''), 100)
        th_last_name = safe_trim(data.get('thLastName', ''), 100)
        en_first_name = safe_trim(data.get('enFirstName', ''), 100)
        en_last_name = safe_trim(data.get('enLastName', ''), 100)
        print("[DEBUG SBA] Personal info extracted")

        # Card info
        print("[DEBUG SBA] Extracting card info")
        card_id_type = {'CITIZEN_CARD': 'C', 'PASSPORT': 'P'}.get(data.get('identificationCardType', ''), 'C')
        card_number = safe_trim(data.get('cardNumber', ''), 50)
        card_issue = format_date(
            data.get('cardIssueDate', {}).get('formatted', '') if data.get('cardIssueDate') else '')
        card_issue = card_issue or ''
        card_expiry = format_date(
            data.get('cardExpiryDate', {}).get('formatted', '') if data.get('cardExpiryDate') else '')
        card_expiry = card_expiry or ''
        print("[DEBUG SBA] Card info extracted")

        # Additional personal info
        print("[DEBUG SBA] Extracting additional personal info")
        gender = data.get('userAuthen', {}).get('gender', 'O')[:1] if isinstance(data.get('userAuthen'), dict) else 'O'
        birthday = format_date(data.get('birthDate', {}).get('formatted', '') if data.get('birthDate') else '')
        birthday = birthday or ''
        print("[DEBUG SBA] Additional personal info extracted")

        # Contact info
        print("[DEBUG SBA] Extracting contact info")
        email = safe_trim(data.get('email', ''), 100)
        mobile = safe_trim(data.get('mobileNumber', ''), 20)
        tel_no1 = safe_trim(data.get('tel', ''), 20)
        tel_no2 = safe_trim(data.get('officeTelephoneNumber', ''), 20)
        fax_no1 = safe_trim(data.get('fax', ''), 20)
        print("[DEBUG SBA] Contact info extracted")

        # Construct address strings
        print("[DEBUG SBA] Constructing address strings")
        first_addr1 = f"{residence['no']} {residence['moo']} {residence['road']}".strip() or ''
        first_addr2 = f"{residence['sub_district']} {residence['district']}".strip() or ''
        first_addr3 = residence['province'].strip() or ''
        first_zipcode = residence['postal_code'].strip() or ''
        first_ctycode = residence['country'].strip() or 'TH'

        second_addr1 = ''
        second_addr2 = ''
        second_addr3 = ''
        second_zipcode = ''
        second_ctycode = ''
        second_telno1 = mobile
        second_telno2 = tel_no1
        second_faxno1 = fax_no1

        third_addr1 = f"{mailing['no']} {mailing['moo']} {mailing['road']}".strip() or ''
        third_addr2 = f"{mailing['sub_district']} {mailing['district']}".strip() or ''
        third_addr3 = mailing['province'].strip() or ''
        third_zipcode = mailing['postal_code'].strip() or ''
        third_ctycode = mailing['country'].strip() or 'TH'
        third_telno1 = mobile
        third_telno2 = tel_no1
        third_faxno1 = fax_no1
        print("[DEBUG SBA] Address strings constructed")

        # Extract banking info
        print("[DEBUG SBA] Extracting banking info")
        bank_code = redemption_accounts.get('bankCode', '')
        bank_branch_code = redemption_accounts.get('bankBranchCode', '')
        bank_acc_type = redemption_accounts.get('bankAccountType', {}).get('key', '1')[:1] if isinstance(
            redemption_accounts.get('bankAccountType'), dict) else '1'
        bank_acc_no = safe_trim(redemption_accounts.get('bankAccountNo', ''), 20)
        print("[DEBUG SBA] Banking info extracted")

        # Extract image paths
        print("[DEBUG SBA] Extracting image paths")
        attachments = data.get('uploadedAttachments', {})
        img_cardid = f'SettradeEOpen/images/{app_id}/140173_nationalIdCard.jpg' if attachments.get(
            '140173_nationalIdCard.jpg') else ''
        img_cardid_face = f'SettradeEOpen/images/{app_id}/140173_selfieNationalIdCard.jpg' if attachments.get(
            '140173_selfieNationalIdCard.jpg') else ''
        img_book_account = f'SettradeEOpen/images/{app_id}/140173_bookbankATS.jpg' if attachments.get(
            '140173_bookbankATS.jpg') else ''
        img_signature = f'SettradeEOpen/images/{app_id}/140173_signature.jpg' if attachments.get(
            '140173_signature.jpg') else ''
        img_slip = f'SettradeEOpen/images/{app_id}/140173_slip.jpg' if attachments.get('140173_slip.jpg') else ''
        print("[DEBUG SBA] Image paths extracted")

        # Extract account types and features
        print("[DEBUG SBA] Extracting account types and features")
        account_types = app_data.get('types', [])
        account_type_str = ','.join(account_types) or ''
        custtype = '1' if 'EQUITY' in account_types or 'EQUITY_CASH_ACCOUNT' in account_types else '4'

        service_type = data.get('serviceType', {}).get('key', 'N')[:1] if isinstance(data.get('serviceType'),
                                                                                     dict) else 'N'
        receive_type = data.get('receiveType', {}).get('key', '02') or '02'
        payment_type = data.get('paymentType', {}).get('key', '02') or '02'

        mkt_id = safe_trim(data.get('referralId', ''), 20)
        broker_id = safe_trim(data.get('brokerId', ''), 20)

        has_cash = 'Y' if 'EQUITY' in account_types or 'EQUITY_CASH_ACCOUNT' in account_types else 'N'
        has_credit = 'Y' if 'CREDIT_BALANCE' in account_types else 'N'
        has_tfex = 'Y' if 'TFEX' in account_types else 'N'
        has_bond = 'Y' if 'BOND' in account_types else 'N'
        has_fund = 'Y' if 'FUND' in account_types else 'N'
        has_offshore = 'Y' if 'OFFSHORE' in account_types else 'N'
        cash_mkt = '0.00'
        cash_rsk = '0.00'
        cash_bal_mkt = '0.00'
        cash_bal_rsk = '0.00'
        credit_bal_mkt = '0.00'
        credit_bal_rsk = '0.00'
        tfex_mkt = '0.00'
        tfex_rsk = '0.00'
        bond_mkt = '0.00'
        bond_rsk = '0.00'
        fund_mkt = '0.00'
        fund_rsk = '0.00'
        offshore_mkt = '0.00'
        offshore_rsk = '0.00'
        print("[DEBUG SBA] Account types and features extracted")

        # Financial info
        print("[DEBUG SBA] Extracting financial info")
        financial_info = {item['questionId']: item['answer'][0]['label'] for item in data.get('financialInfo', []) if
                          item.get('answer')}
        occupation = financial_info.get('occupationId', '')
        company_name = financial_info.get('companyName', '')
        position = financial_info.get('position', '')
        monthly_income = financial_info.get('monthlyIncomeLevel', '')
        income_source = financial_info.get('incomeSource', '')
        income_country = financial_info.get('incomeSourceCountry', '')
        asset_value = financial_info.get('assetValue', '')
        print("[DEBUG SBA] Financial info extracted")

        # Family info
        print("[DEBUG SBA] Extracting family info")
        family_info = data.get('familyInfo', {})
        marital_status = family_info.get('maritalStatus', {}).get('key', 'Single')
        spouse_tname = safe_trim(family_info.get('spouseThFirstName', ''), 100)
        spouse_tsurname = safe_trim(family_info.get('spouseThLastName', ''), 100)
        spouse_ename = safe_trim(family_info.get('spouseEnFirstName', ''), 100)
        spouse_esurname = safe_trim(family_info.get('spouseEnLastName', ''), 100)
        spouse_cardid = safe_trim(family_info.get('spouseCardNumber', ''), 50)
        print("[DEBUG SBA] Family info extracted")

        # Children info
        print("[DEBUG SBA] Extracting children info")
        children_info = data.get('childrenInfo', {})
        children_amount = children_info.get('childrenAmount', {}).get('key', '0')
        print("[DEBUG SBA] Children info extracted")

        # Other contact info
        print("[DEBUG SBA] Extracting other contact info")
        other_contact = {item['questionId']: item['answer'][0]['label'] for item in data.get('otherContactInfo', []) if
                         item.get('answer')}
        emergency_name = safe_trim(other_contact.get('name', ''), 100)
        emergency_surname = safe_trim(other_contact.get('lastName', ''), 100)
        emergency_relation = safe_trim(other_contact.get('relation', ''), 50)
        emergency_tel = safe_trim(other_contact.get('telRelation', ''), 20)
        print("[DEBUG SBA] Other contact info extracted")

        # Declaration info
        print("[DEBUG SBA] Extracting declaration info")
        declaration_info = {item['questionId']: item['answer'][0]['label'] for item in data.get('declarationInfo', [])
                            if item.get('answer')}
        investment_objective = declaration_info.get('investmentObjective', '')
        political_person = 'N' if declaration_info.get('politicalRelatedPerson', 'ไม่ใช่') == 'ไม่ใช่' else 'Y'
        investment_experience = declaration_info.get('investmentObjectiveOther', '')
        reject_financial = 'N' if declaration_info.get('rejectFinancial', 'ไม่ใช่') == 'ไม่ใช่' else 'Y'
        money_laundering = 'N' if declaration_info.get('moneyLaundering', 'ไม่ใช่') == 'ไม่ใช่' else 'Y'
        print("[DEBUG SBA] Declaration info extracted")

        # Additional fields
        print("[DEBUG SBA] Setting additional fields")
        reverse = ''
        remark = ''
        notes = ''
        rsk_notes = ''
        rsk_datetime = None
        hrs_datetime = None
        flag_export = 'N'
        flag_export_user = ''
        flag_export_datetime = None
        last_entry_user = ''
        last_entry_datetime = None
        mktid_entry_user = ''
        mktid_entry_datetime = None
        flag_reject = 'N'
        flag_reject_notes = ''
        flag_reject_user = ''
        flag_reject_datetime = None
        stt_update_status = ''
        stt_update_status_user = ''
        stt_update_status_datetime = None
        ddr_status = app_data.get('ddrStatus', '')
        ddr_status_datetime = None
        print("[DEBUG SBA] Additional fields set")

        # Additional NOT NULL fields from schema
        print("[DEBUG SBA] Setting NOT NULL fields")
        custgrp = 'U'
        custcode = 'UNKNOWN'  # แทนที่ '' เพื่อหลีกเลี่ยงข้อผิดพลาด NOT NULL
        docaddr = '1'
        eopen_type = 'S'
        appcredit_cb = '0'  # แทนที่ '' เพื่อหลีกเลี่ยงข้อผิดพลาด NOT NULL
        appcredit_cashb = '0'  # แทนที่ '' เพื่อหลีกเลี่ยงข้อผิดพลาด NOT NULL
        appcredit_f = '0'  # แทนที่ '' เพื่อหลีกเลี่ยงข้อผิดพลาด NOT NULL
        appcredit_i = '0'  # แทนที่ '' เพื่อหลีกเลี่ยงข้อผิดพลาด NOT NULL
        appcredit_g = '0'  # แทนที่ '' เพื่อหลีกเลี่ยงข้อผิดพลาด NOT NULL
        flag_ca = 'N'
        flag_aom = 'N'
        print("[DEBUG SBA] NOT NULL fields set")

        # Current date for transaction date
        print("[DEBUG SBA] Setting transaction date")
        trans_date = datetime.now().strftime('%Y-%m-%d')
        request_time = datetime.now().strftime('%Y%m%d%H%M%S')
        entry_datetime = datetime.now()
        entry_datetime_str = format_datetime(entry_datetime)
        print("[DEBUG SBA] Transaction date set")

        # Define columns and values
        columns = [
            'trans_date', 'request_time', 'custtype', 'accounttype',
            'ttitle', 'tname', 'tsurname', 'etitle', 'ename', 'esurname',
            'cardidtype', 'cardid', 'cardissue', 'cardexpire', 'sex', 'birthday',
            'firstaddr1', 'firstaddr2', 'firstaddr3', 'firstzipcode', 'firstctycode',
            'firsttelno1', 'firsttelno2', 'firstfaxno1', 'email1',
            'secondaddr1', 'secondaddr2', 'secondaddr3', 'secondzipcode', 'secondctycode',
            'secondtelno1', 'secondtelno2', 'secondfaxno1',
            'thirdaddr1', 'thirdaddr2', 'thirdaddr3', 'thirdzipcode', 'thirdctycode',
            'thirdtelno1', 'thirdtelno2', 'thirdfaxno1',
            'reverse', 'remark',
            'bankcode', 'bankbranchcode', 'bankacctype', 'bankaccno',
            'receivetype', 'paymenttype', 'servicetype', 'mktid',
            'custgrp', 'custcode', 'docaddr',
            'appcredit_cb', 'appcredit_cashb', 'appcredit_f', 'appcredit_i', 'appcredit_g',
            'eopen_type',
            'img_cardid', 'img_cardid_face', 'img_book_account',
            'cash_type', 'cash_mkt', 'cash_rsk',
            'cash_bal_type', 'cash_bal_mkt', 'cash_bal_rsk',
            'credit_bal_type', 'credit_bal_mkt', 'credit_bal_rsk',
            'tfex_type', 'tfex_mkt', 'tfex_rsk',
            'bond_type', 'bond_mkt', 'bond_rsk',
            'fund_type', 'fund_mkt', 'fund_rsk',
            'offshore_type', 'offshore_mkt', 'offshore_rsk',
            'notes', 'rsk_notes', 'rsk_datetime', 'hrs_datetime',
            'flag_export', 'flag_export_user', 'flag_export_datetime',
            'is_active', 'entry_user', 'entry_datetime',
            'last_entry_user', 'last_entry_datetime',
            'mktid_entry_user', 'mktid_entry_datetime',
            'flag_ca', 'flag_aom',
            'flag_reject', 'flag_reject_notes', 'flag_reject_user', 'flag_reject_datetime',
            'stt_update_status', 'stt_update_status_user', 'stt_update_status_datetime',
            'ddr_bank_code', 'ddr_bank_account_no', 'ddr_status', 'ddr_status_datetime'
        ]

        values = (
            trans_date, request_time, custtype, account_type_str,
            title, th_first_name, th_last_name, etitle, en_first_name, en_last_name,
            card_id_type, card_number, card_issue, card_expiry, gender, birthday,
            first_addr1, first_addr2, first_addr3, first_zipcode, first_ctycode,
            tel_no1, tel_no2, fax_no1, email,
            second_addr1, second_addr2, second_addr3, second_zipcode, second_ctycode,
            second_telno1, second_telno2, second_faxno1,
            third_addr1, third_addr2, third_addr3, third_zipcode, third_ctycode,
            third_telno1, third_telno2, third_faxno1,
            reverse, remark,
            bank_code, bank_branch_code, bank_acc_type, bank_acc_no,
            receive_type, payment_type, service_type, mkt_id,
            custgrp, custcode, docaddr,
            appcredit_cb, appcredit_cashb, appcredit_f, appcredit_i, appcredit_g,
            eopen_type,
            img_cardid, img_cardid_face, img_book_account,
            has_cash, cash_mkt, cash_rsk,
            has_cash, cash_bal_mkt, cash_bal_rsk,
            has_credit, credit_bal_mkt, credit_bal_rsk,
            has_tfex, tfex_mkt, tfex_rsk,
            has_bond, bond_mkt, bond_rsk,
            has_fund, fund_mkt, fund_rsk,
            has_offshore, offshore_mkt, offshore_rsk,
            notes, rsk_notes, rsk_datetime, hrs_datetime,
            flag_export, flag_export_user, flag_export_datetime,
            str(1), 'SYSTEM', entry_datetime_str,
            last_entry_user, last_entry_datetime,
            mktid_entry_user, mktid_entry_datetime,
            flag_ca, flag_aom,
            flag_reject, flag_reject_notes, flag_reject_user, flag_reject_datetime,
            stt_update_status, stt_update_status_user, stt_update_status_datetime,
            ddr_bank, safe_trim(ddr_bank_account_no, 20), ddr_status, ddr_status_datetime
        )

        print(f"[DEBUG SBA] Number of columns: {len(columns)}")
        print(f"[DEBUG SBA] Number of values: {len(values)}")
        if len(columns) != len(values):
            print("[DEBUG SBA] Error: Number of columns and values do not match")
            return False

        print("[DEBUG SBA] Constructing INSERT query")
        columns_str = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))
        insert_query = f"INSERT INTO public.eopen_sba ({columns_str}) VALUES ({placeholders})"
        print(f"[DEBUG SBA] INSERT query: {insert_query}")

        print("[DEBUG SBA] Insert values:")
        for i, v in enumerate(values):
            print(f"  [{i}] {v} ({type(v).__name__}) len={len(str(v)) if v is not None else 0}")

        if check_values_for_percent(values):
            print("[DEBUG SBA] Found '%' in values, which may cause string formatting issues")

        print("[DEBUG SBA] Executing query")
        try:
            cursor.execute(insert_query, values)
            print("[DEBUG SBA] Query executed")
        except Exception as e:
            print(f"[DEBUG SBA] Detailed error during query execution: {e}")
            print(f"[DEBUG SBA] Query: {insert_query}")
            print("[DEBUG SBA] Values types:")
            for i, v in enumerate(values):
                print(f"  [{i}] {type(v).__name__}")
            raise

        print("[DEBUG SBA] Committing transaction")
        connection.commit()
        print(f"Successfully inserted data into eopen_sba for app_id: {app_id}")
        return True

    except Exception as e:
        print(f"Error inserting data into eopen_sba: {e}")
        connection.rollback()
        return False
    finally:
        if 'cursor' in locals():
            print("[DEBUG SBA] Closing cursor")
            cursor.close()
        else:
            print("[DEBUG SBA] Cursor was not created")

def insert_stt_data(json_data, connection):
    """Insert data into eopen_stt table using parameterized query"""
    print("[DEBUG STT] Starting insert_stt_data function")
    if not json_data or not connection:
        print("No JSON data or database connection")
        return False
    print("[DEBUG STT] JSON data and connection are valid")

    try:
        print("[DEBUG STT] Creating cursor")
        cursor = connection.cursor()

        print("[DEBUG STT] Extracting app_data")
        app_data = json_data.get('appId', {})
        data = app_data.get('data', {})
        print("[DEBUG STT] App_data extracted")

        print("[DEBUG STT] Validating app_id")
        app_id = app_data.get('applicationId')
        if app_id is None:
            print("Error: app_id is required but missing in JSON")
            return False
        app_id = int(app_id)
        print(f"[DEBUG STT] app_id: {app_id}")

        print("[DEBUG STT] Setting NOT NULL fields")
        trans_date = datetime.now().strftime('%Y-%m-%d')
        request_time = datetime.now().strftime('%Y%m%d%H%M%S')
        flag_process = 'B'
        print("[DEBUG STT] NOT NULL fields set")

        print("[DEBUG STT] Extracting application info")
        status = safe_trim(app_data.get('status', ''), 50)
        types = ','.join(app_data.get('types', [])) or ''
        print("[DEBUG STT] Application info extracted")

        print("[DEBUG STT] Extracting Thai personal info")
        title_t = transform_title(data.get('title', {}).get('key', '') if isinstance(data.get('title'), dict) else '')
        th_first_name = safe_trim(data.get('thFirstName', ''), 50)
        th_last_name = safe_trim(data.get('thLastName', ''), 50)
        print("[DEBUG STT] Thai personal info extracted")

        print("[DEBUG STT] Extracting English personal info")
        title_e = transform_etitle(data.get('title', {}).get('key', '') if isinstance(data.get('title'), dict) else '')
        en_first_name = safe_trim(data.get('enFirstName', ''), 50)
        en_last_name = safe_trim(data.get('enLastName', ''), 50)
        print("[DEBUG STT] English personal info extracted")

        print("[DEBUG STT] Extracting contact info")
        mobile = safe_trim(data.get('mobileNumber', ''), 20)
        email = safe_trim(data.get('email', ''), 100)
        print("[DEBUG STT] Contact info extracted")

        print("[DEBUG STT] Extracting ID card info")
        card_type = safe_trim(data.get('identificationCardType', ''), 20)
        card_issue_date_raw = data.get('cardIssueDate', {}).get('formatted', '') if data.get('cardIssueDate') else ''
        card_issue_date = format_date(card_issue_date_raw) or ''
        card_expiry_date_raw = data.get('cardExpiryDate', {}).get('formatted', '') if data.get('cardExpiryDate') else ''
        card_expiry_date = format_date(card_expiry_date_raw) or ''
        print("[DEBUG STT] ID card info extracted")

        print("[DEBUG STT] Extracting timestamps")
        created_time = safe_trim(app_data.get('createdTime', ''), 50)
        last_updated_time = safe_trim(app_data.get('lastUpdatedTime', ''), 50)
        submitted_time = safe_trim(app_data.get('submittedTime', ''), 50)
        print("[DEBUG STT] Timestamps extracted")

        print("[DEBUG STT] Extracting verification and contract info")
        verifi_type = safe_trim(app_data.get('verificationType', ''), 50)
        contract_no = safe_trim(app_data.get('contractNo', ''), 20)
        print("[DEBUG STT] Verification and contract info extracted")

        print("[DEBUG STT] Extracting user info")
        u_userid_raw = data.get('userAuthen', {}).get('userId')
        u_userid = int(u_userid_raw) if u_userid_raw is not None else None
        u_cid = safe_trim(data.get('cardNumber', ''), 50)
        print("[DEBUG STT] User info extracted")

        print("[DEBUG STT] Extracting additional personal info")
        gender = data.get('userAuthen', {}).get('gender', 'O') if isinstance(data.get('userAuthen'), dict) else 'O'
        nationality = safe_trim(data.get('nationality', ''), 50)
        taxid = safe_trim(data.get('cardNumber', ''), 50)
        birth_date_raw = data.get('birthDate', {}).get('formatted', '') if data.get('birthDate') else ''
        birth_date = format_date(birth_date_raw) or ''
        print("[DEBUG STT] Additional personal info extracted")

        print("[DEBUG STT] Setting audit fields")
        is_active = 1
        entry_user = 'SYSTEM'
        entry_datetime = datetime.now()
        print("[DEBUG STT] Audit fields set")

        print("[DEBUG STT] Preparing INSERT query")
        insert_query = """
        INSERT INTO public.eopen_stt (
            trans_date, request_time, flag_process, app_id, status, types,
            t_title, t_fname, t_lname, e_title, e_fname, e_lname,
            mobile, email, id_card_type, card_issue_date, card_expiry_date,
            created_time, last_updated_time, submitted_time,
            verifi_type, contract_no, u_userid, u_cid, gender, nationality, taxid, birth_date,
            is_active, entry_user, entry_datetime
        ) VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s
        )
        """
        print("[DEBUG STT] INSERT query prepared")

        print("[DEBUG STT] Preparing values tuple")
        values = (
            trans_date, request_time, flag_process, app_id, status, types,
            title_t, th_first_name, th_last_name, title_e, en_first_name, en_last_name,
            mobile, email, card_type, card_issue_date, card_expiry_date,
            created_time, last_updated_time, submitted_time,
            verifi_type, contract_no, u_userid, u_cid, gender, nationality, taxid, birth_date,
            is_active, entry_user, entry_datetime
        )
        print("[DEBUG STT] Values tuple prepared")

        print("[DEBUG STT] Insert values:")
        for i, v in enumerate(values):
            print(f"  [{i}] {v} ({type(v).__name__}) len={len(str(v)) if v is not None else 0}")

        print("[DEBUG STT] Executing query")
        cursor.execute(insert_query, values)
        print("[DEBUG STT] Query executed")

        print("[DEBUG STT] Committing transaction")
        connection.commit()
        print(f"Successfully inserted data into eopen_stt for app_id: {app_id}")
        return True

    except Exception as e:
        print(f"Error inserting data into eopen_stt: {e}")
        connection.rollback()
        return False
    finally:
        if 'cursor' in locals():
            print("[DEBUG STT] Closing cursor")
            cursor.close()
        else:
            print("[DEBUG STT] Cursor was not created")

def main():
    # Read JSON file
    json_data = read_json_file('data.json')
    if not json_data:
        print("Failed to read JSON file")
        return

    # Connect to database
    connection = connect_db()
    if not connection:
        print("Failed to connect to database")
        return

    try:
        # Insert data into tables
        print("[DEBUG MAIN] Calling insert_sba_data")
        sba_success = insert_sba_data(json_data, connection)
        print("[DEBUG MAIN] insert_sba_data completed, result:", sba_success)

        print("[DEBUG MAIN] Calling insert_stt_data")
        stt_success = insert_stt_data(json_data, connection)
        print("[DEBUG MAIN] insert_stt_data completed, result:", stt_success)

        if sba_success and stt_success:
            print("Data successfully inserted into both tables")
        else:
            print("Error occurred while inserting data")

    finally:
        if connection:
            connection.close()
            print("Database connection closed")

if __name__ == "__main__":
    main()