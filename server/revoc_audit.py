import json
import logging
import os
import csv


LOGGER = logging.getLogger(__name__)

INDY_TXN_TYPES = {
    "0": "NODE",
    "1": "NYM",
    "3": "GET_TXN",
    "4": "TXN_AUTHOR_AGREEMENT",
    "5": "TXN_AUTHOR_AGREEMENT_AML",
    "6": "GET_TXN_AUTHOR_AGREEMENT",
    "7": "GET_TXN_AUTHOR_AGREEMENT_AML",
    "100": "ATTRIB",
    "101": "SCHEMA",
    "102": "CRED_DEF",
    "103": "DISCLO",
    "104": "GET_ATTR",
    "105": "GET_NYM",
    "107": "GET_SCHEMA",
    "108": "GET_CLAIM_DEF",
    "109": "POOL_UPGRADE",
    "110": "NODE_UPGRADE",
    "111": "POOL_CONFIG",
    "112": "CHANGE_KEY",
    "113": "REVOC_REG_DEF",
    "114": "REVOC_REG_ENTRY",
    "115": "GET_REVOC_REG_DEF",
    "116": "GET_REVOC_REG",
    "117": "GET_REVOC_REG_DELTA",
    "118": "POOL_RESTART",
    "119": "VALIDATOR_INFO",
    "120": "AUTH_RULE",
    "121": "GET_AUTH_RULE",
    "122": "AUTH_RULES",
}

INDY_ROLE_TYPES = {"0": "TRUSTEE", "2": "STEWARD", "100": "TGB", "101": "ENDORSER"}


TXN_FILE = "./server/txns.txt"
REVOC_REG = "4xE68b6S5VRFrKMMG1U95M:4:4xE68b6S5VRFrKMMG1U95M:3:CL:59232:default:CL_ACCUM:4ae1cc6c-f6bd-486c-8057-88f2ce74e960"
WALLET_REVOC = [115,197,18,12,121,106,192,70,167,147,176,188,136,16,172,142,4,17,177,194,204,195,110,67,191,164,206,33,146,84,141,173,180,72,209,199,196,114,174,179,13,155,65,211,178,207,32,156,170,45,151,189,113,80,62,183,218,123,96,186,34,118,175,15,64,190,185,127,181,210,187,26,161,182,201,152,159,193,135,103,101,9,29,93,129,143,89,150,97,81,14,98,69,10,140,27,11]
WALLET_ACCUM = "21 125F8E905EFE2EC01BA83FAFE1A21A3B95AD7D04228F1C4319E257D3A6BFAED55 21 11DB00EE7FD06BDEEFBFDB2FD845C9685789289CFCFBC1EA5ABAC6795F89B65CE 6 76973C3F4785158DCF3C66A059FD2B1E3C65B8292B1475BB95A1E2981EA6AC2A 4 0A4568F9398F0745D3F86C83622F5F89912D3973DE0DAC865EF7F69F437334CF 6 80C8727BE412B2C334F85FFF03D5DFECB01B48A4E540022AA0D948076A859B23 4 25BE811E42EA6E9F5BAF2F0C2DDAD25F41F338F17C3013B919CD6A1BE45683D4"


if __name__ == "__main__":
    all_revoked = []
    with open(TXN_FILE, 'r', newline='') as txn_file:
        csvreader = csv.reader(txn_file, delimiter=',', quotechar='"', escapechar='\\')
        for row in csvreader:
            ledger_type = row[0]
            txn_seqno = row[1]
            txn_type = row[2]
            txn_id = row[3]
            txn_date = row[4]
            txn_json = json.loads(row[5])
            terms_id = row[6]
            if txn_type == "113" and txn_json["txnMetadata"]["txnId"] == REVOC_REG:
	            print(txn_seqno, txn_type)
            elif txn_type == "114" and txn_json["txnMetadata"]["txnId"] == "5:"+REVOC_REG:
                accum = txn_json["txn"]["data"]["value"]["accum"]
                prev_accum = txn_json["txn"]["data"]["value"]["prevAccum"] if "prevAccum" in txn_json["txn"]["data"]["value"] else ""
                revoked = txn_json["txn"]["data"]["value"]["revoked"] if "revoked" in txn_json["txn"]["data"]["value"] else []
                all_revoked.extend(revoked)
                print(txn_seqno, ",", txn_type, ",", revoked, ",", accum, ",", prev_accum)
    all_revoked.sort()
    WALLET_REVOC.sort()
    print("ALL:", all_revoked)
    print("WAL:", WALLET_REVOC)
    print("WAL:", WALLET_ACCUM)
