import os, sys
import W_utility.file as ufile
from W_utility.log import ext_print
import W_utility.mysql as mysql

db = mysql._MySQL('localhost', 3306, 'root', 'qateam', 'pubmed')

def Insert_DB(fin):
    for root, dir, files in os.walk(fin):
        for f in files:
            if not f.endswith(".csv"):
                continue
            print ext_print(f)

            output = []
            # read input data
            fdin = os.path.join(root, f)
            rows = ufile.read_csv(fdin)
            for row in rows:
                # param = (PMID, JournalTitle, PubDate, ArticleTitle, Abstract, Keywords)
                PubDate = row[2]

                if PubDate != '2009':  # To split tasks into differnt machines with MySQL, process tables separatly
                    continue
                table = "article_" + PubDate
                #
                # if (row[2] == '' or row[2] is None): PubDate = 0
                # PubDate = int(PubDate)
                # table = 'article_0-1950'
                # if 2000 >= PubDate >= 1951:
                #     table = 'article_1951-2000'
                # if 2005 >= PubDate >= 2001:
                #     table = 'article_2001-2005'
                # elif PubDate > 2005:
                #     table = 'article_'+ str(PubDate)
				
                param = (row[0], row[1], PubDate, row[3], row[4], row[5])
                sql = "INSERT INTO `" + table + "` (`PMID`, `JournalTitle`, `PubDate`, `ArticleTitle`, `Abstract`, `Keywords`) VALUES(%s, %s, %s, %s, %s, %s);"
                msg = db.execute(sql, param)
                if msg != 1: print msg

    print ext_print('all tasks completed\n')
    return True


# processing the command line options
import argparse


def _process_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', default=r'D:\Users\Tony\extracted_1-1076', help='file with the list of trials')
    return parser.parse_args(sys.argv[1:])


if __name__ == '__main__':
    print ''
    args = _process_args()
    Insert_DB(args.i)
    print ''
