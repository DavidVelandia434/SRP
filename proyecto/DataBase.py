import gzip

f = gzip.open("title.basics.tsv.gz", "rt", encoding="utf-8")

content = f.readline().strip().split('\t')

f.close()


print(content)