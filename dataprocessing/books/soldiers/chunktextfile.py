import re
from interface.chunktextinterface import ChunkTextInterface

class ChunkTextFile(ChunkTextInterface):

    def chunk_text(self, text):
        text = re.sub(r"(?:<|>|&|'|)", r"", text)
        #tag stuff:
        sotilas = r"(?:\W|\d){1,5}((?!(?:AAL|SPOIK|AUL|AKE|AKM|AKL|APT|AKK|AOK|AUK|AAUK|EKM|ELK|ETP|FFB|HRUP|HTK|HKI|HRE|HRR|HKKK|IPA|IPE|IPK|IIK|JBK|JKL|JKV|KEK|KHK|KKK|KAL|KKP|KLP|KTA|KOK|KTR|KTP|KTV|LKV|LLP|LRE|LVK|OKH|OKL|OKM|OKW|PIM|PPK|PPP|PLL|PTK|PYS|PYP|RAUL|RJR|RKJ|RKK|RTR|RUK|RVP|RVL|SKK|URR|VKM|MKL|MSK|MKUL|MLL|MTK|KTK|PBH|NPOR|RUL|SAK|SLL|RTVL|IPAK|SDP|SKL|SUL|STS|SNL|SML|SMP|SNS|SKP|KVL|SVR|SVJ|SVUL|SVML|STKL|SPR|SRL|SLR|SKDL|SUL|STL|KOP|SEL|SOP|SOL|SAL|SOK|STTK|SPL|SKT|TVO|TVK|TUL|TTPS|SKTL|OTK|USA|VPK|VVL|VVP|VII|SHL|IIKT|KORPR|VVL|EKIII|STIK|XXX)\b)[A-ZÄ-Öln-]{3,})\b"
        text = re.sub(sotilas, r"\n</PERSON>\n\n<PERSON>\1", text)
        #text = re.sub(ur"(?:\W|\d){1,5}((?!(?:[BDHJKLMNPRSTVWFGZX].[BDHJKLMNPRSTVWFGZX]|[BDHJKLMNPRSTVWFGZX][BDHJKLMNPRSTVWFGZX].|.[BDHJKLMNPRSTVWFGZX][BDHJKLMNPRSTVWFGZX]|IPAK|RAUL|IIKT|KORPR|EKIII|SPOIK|PIOn|AAUK).?\b)[A-ZÄ-Öln-]{4,}|AHO)\b", ur"\n</PERSON>\n\n<PERSON>\1", text)
        text = "<DATA>\n<PERSON>\n" + text + "</PERSON>\n</DATA>"
        return text


