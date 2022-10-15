class cls_query:
    def __init__(self) -> None:
        pass
        
    def __iter__(self):
        for item in self.ls_query:
            for rt in self.retweet:
                str_rt = self.f_rtToStr(rt)
                yield ((item[0],item[1]), (str_rt, rt))

    def __len__(self):
        return len(self.ls_query)*len(self.retweet)

    def f_rtToStr(self, isRT):
        return "_with_rt_" if isRT else "_no_rt_"

    def f_getKey(self, query, isRT):
        for item in self.ls_query:
            if query == item[1]:
                return (item[0], self.f_rtToStr(isRT))

class cls_qTrackHash(cls_query):
    k_sharifUni = "sharif_uni"
    v_sharifUni = "#دانشگاه_شریف"
    k_etesabat = "etesabat_sarasari"
    v_etesabat = "#اعتصابات_سراسری"
    ls_query = [
        (k_sharifUni,v_sharifUni),
        (k_etesabat,v_etesabat)
        ]
    retweet = [True,False]
class cls_qMAmini:
    v_maminiFA = "#مهسا_امینی"
    v_maminiEN = "#MahsaAmini"
    k_maminiAll = "mamini_all"
    k_maminiFA = "mamini_fa"
    k_maminiEN = "mamini_en"
    v_maminiAll = "(" + v_maminiFA + " OR " + v_maminiEN + ")"
    ls_query = [(k_maminiFA,v_maminiFA), 
        (k_maminiEN,v_maminiEN), 
        (k_maminiAll, v_maminiAll)
        ]
    retweet = [True,False]
    
    def __init__(self) -> None:
        pass
        
    def __iter__(self):
        for item in self.ls_query:
            for rt in self.retweet:
                str_rt = self.f_rtToStr(rt)
                yield ((item[0],item[1]), (str_rt, rt))

    def __len__(self):
        return len(self.ls_query)*len(self.retweet)

    def f_rtToStr(self, isRT):
        return "_with_rt_" if isRT else "_no_rt_"

    def f_getKey(self, query, isRT):
        for item in self.ls_query:
            if query == item[1]:
                return (item[0], self.f_rtToStr(isRT))
    
    