# 001 - 099     Account status type codes
# 100           Total Credits summary type code
# 101-399       Credit summary and detail type codes
# 400           Total Debits summary type codes
# 401-699       Debit summary and detail type codes
# 700-999       Customized/Proprietary Type Codes


bai_code_descriptions = {
    "010": "Opening Ledger Balance",
    "015": "Closing Ledger Balance",
    "040": "Opening Ledger Balance Previous Day",
    "045": "Closing Ledger Balance Previous Day",
    "072": "Total Credit Amount MTD",
    "074": "Float Adjustment",
 
    "100": "Total Credits",

# 101-399       Credit summary and detail type codes

    "110": "Credit Customer Originated",
    "120": "Treasury Management Credit",
    "140": "ACH Credit",
    "150": "ACH Return Item Credit",
    "158": "Real Time Payment Credit",
    "159": "Miscellaneous Credit",
    "164": "Corporate Trade Payment Credit",
    "165": "Preauthorized ACH Credit",
    "166": "ACH Settlement Credit",
    "170": "Credit Card Deposit",
    "180": "Wire Transfer Credit",
    "186": "Securities Interest Credit",
    "187": "Cash Letter Pre-Encoded Dep CR",
    "190": "Incoming Money Transfer",
    "191": "Individual Incoming INTERNAL Money TRF",
    "195": "Incoming Money Transfer Credit",
    "200": "Standard Check Deposit",
    "201": "Individual Auto Transfer CR",
    "210": "Check Collection Credit",
    "239": "Miscellaneous Deposit Credit",
    "250": "Cash Deposit Credit",
    "255": "Check Posted and Returned CR",
    "260": "ATM Deposit Credit",
    "270": "ZBA Check Deposit",
    "275": "ZBA Credit",
    "280": "Branch Deposit Credit",
    "294": "Incoming International Credit",
    "301": "Commercial Deposit Credit",
    "310": "Commercial Check Credit",
    "350": "Investment Credit",
    "390": "Miscellaneous Credit",

    "400": "Total Debits",

# 401-699       Debit summary and detail type codes

    "412": "Debit Adjustment",
    "416": "Threshold Debit",
    "420": "Treasury Management Debit",
    "450": "ACH Return Item Debit",
    "455": "Preauthorized ACH Debit",
    "459": "Miscellaneous ACH Debit",
    "470": "Cash Letter Debit",
    "475": "Checks Paid Debit",
    "480": "Bank Draft Debit",
    "486": "Foreign Letter of Credit",
    "490": "Miscellaneous Debit",
    "491": "Outgoing Internl Money Trnsfr",
    "495": "Outgoing Money Transfer Debit",
    "500": "Commercial Withdrawal",
    "500": "Commercial Withdrawal",
    "501": "Individual Auto Transfer DR",
    "530": "Branch Withdrawal Debit",
    "539": "Miscellaneous Withdrawal",
    "550": "Investment Debit",
    "555": "Deposited Item Return Debit",
    "561": "Account Analysis Fee Debit",
    "570": "ZBA Withdrawal",
    "575": "ZBA Debit",
    "580": "Branch Withdrawal",
    "594": "Outgoing International Debit",
    "596": "International Service Charge",
    "650": "Overdraft Interest Charge",
    "661": "Credit Card Payment",
    "690": "Miscellaneous Fee",

# 700-999       Customized/Proprietary Type Codes

    "856": "Dep+ Transfer Credit",
    "868": "Dep+ Transfer Debit",
    "906": "Bank Statement",
    "907": "Bank Statement - Special"
}

bai_identifiers = {
    "01": "File Header Record",      # Contains sender/receiver info and file creation date
    "02": "Group Header Record",     # Contains originator/destination and group status
    "03": "Account Identifier",      # Contains account number and currency info
    "16": "Transaction Detail",      # Contains individual transaction details
    "88": "Continuation Record",     # Used when data exceeds record length
    "99": "File Trailer Record",     # End of file marker with control totals
}