from collections import namedtuple
class cls_query:
    def __init__(self) -> None:
        self.m_query = namedtuple("query", ["key","data"])
        self.m_queries = None
        self.m_isRetweet = [True,False]
        
    def __iter__(self):
        for item in self.m_queries:
            for rt in self.m_isRetweet:
                str_rt = self.f_rtToStr(rt)
                yield ((item[0],item[1]), (str_rt, rt))

    def __len__(self):
        return len(self.m_queries)*len(self.m_isRetweet)

    def f_rtToStr(self, isRT):
        return "_with_rt_" if isRT else "_no_rt_"

    def f_getKey(self, query, isRT):
        for item in self.m_queries:
            if query == item[1]:
                return (item[0], self.f_rtToStr(isRT))

class cls_qTrackHash(cls_query):

    def __init__(self) -> None:
        super().__init__()

        self.m_isRetweet = [True]

        self.m_queries = [
            self.m_query("masmumiat_daneshamooz", "#مسمومیت_دانش_آموزان"),
            self.m_query("hamle_chemi_madares", "#حمله_شیمیایی_به_مدارس"),
            #self.m_query("sharif_uni" , "#دانشگاه_شریف") ,
            self.m_query("etesabat_sarasari", "#اعتصابات_سراسری")
              ]

    #k_sharifUni = "sharif_uni"
    #v_sharifUni = "#دانشگاه_شریف"
    #k_etesabat = "etesabat_sarasari"
    #v_etesabat = "#اعتصابات_سراسری"
        #(k_sharifUni,v_sharifUni),
        #(k_etesabat,v_etesabat)
        #]
class cls_qMAmini(cls_query):
   
    
    def __init__(self) -> None:
        super().__init__()

        v_maminiFA = "#مهسا_امینی"
        v_maminiEN = "#MahsaAmini"
        self.m_queries = [
            self.m_query("mamini_fa", v_maminiFA) ,
            self.m_query("mamini_en", v_maminiEN),
            self.m_query("mamini_all", "(" + v_maminiFA + " OR " + v_maminiEN + ")")
              ]