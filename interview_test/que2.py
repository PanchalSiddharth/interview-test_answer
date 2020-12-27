def maxValue(d):
	v=list(d.values())
	k=list(d.keys())
	m=max(v)
	index=k[v.index(m)]
	dic={index:m}
	return dic

dict={"1":5,"2":8,"3":12}
print(maxValue(dict))