# import nltk
#
# dwlr = nltk.downloader.Downloader()
#
# # chunkers, corpora, grammars, help, misc,
# # models, sentiment, stemmers, taggers, tokenizers
# for pkg in dwlr.packages():
#     if pkg.subdir== 'taggers':
#         dwlr.download(pkg.id)
import nltk
print(nltk.__file__)
if sys.platform.startswith('win'):
    # Common locations on Windows:
    path += [
        str(r'C:\nltk_data'), str(r'D:\nltk_data'), str(r'E:\nltk_data'),
        os.path.join(sys.prefix, str('nltk_data')),
        os.path.join(sys.prefix, str('lib'), str('nltk_data')),
        os.path.join(os.environ.get(str('APPDATA'), str('C:\\')), str('nltk_data'))
    ]
else:
    # Common locations on UNIX & OS X:
    path += [
        str('/usr/share/nltk_data'),
        str('/usr/local/share/nltk_data'),
        str('/usr/lib/nltk_data'),
        str('/usr/local/lib/nltk_data')
    ]