from collections import namedtuple
class cls_query:
    def __init__(self) -> None:
        #self.m_query = namedtuple("query", ["key","data"])
        self.m_queries = dict()
        self.m_isRetweet = [True,False]
        
    def __iter__(self):
        for item in self.m_queries.items():
            for rt in self.m_isRetweet:
                str_rt = self.f_rtToStr(rt)
                yield ((item[0], item[1]), (str_rt, rt))

    def __len__(self):
        return len(self.m_queries)*len(self.m_isRetweet)

    def f_rtToStr(self, isRT):
        return "_with_rt_" if isRT else "_no_rt_"

    def f_getKey(self, query, isRT):
        for item in self.m_queries.items():
            if query == item[1][0]:
                return (item[0], self.f_rtToStr(isRT))

class cls_qTrackHash(cls_query):

    def __init__(self) -> None:
        super().__init__()

        self.m_isRetweet = [True]

        self.m_queries = {
            "masmumiat_daneshamooz": ["#مسمومیت_دانش_آموزان", "2023-02-01T00:00:00Z"],
            "hamle_chemi_madares": ["#حمله_شیمیایی_به_مدارس", "2023-02-01T00:00:00Z"],
            "etesabat_sarasari": ["#اعتصابات_سراسری", "2022-09-14T00:00:00Z"],
        }

class cls_qMAmini(cls_query):
   
    def __init__(self) -> None:
        super().__init__()

        self.v_maminiFA = "#مهسا_امینی"
        self.v_maminiEN = "#MahsaAmini"
        self.v_maminiAll = "(" + self.v_maminiFA + " OR " + self.v_maminiEN + ")"
        
        self.m_queries = {
            "mamini_fa": [self.v_maminiFA],
            "mamini_en": [self.v_maminiEN],
            "mamini_all": [self.v_maminiAll] , 
        }