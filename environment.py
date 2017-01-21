PATH = 'data/'
PATH_OUTPUT = PATH+'output/'
PATH_INPUT  = PATH+'input/'
SRT_FOLDER = PATH_INPUT+'srt/'
TAG_FOLDER = PATH_OUTPUT+'tag/'

##*****--  INPUT --******##

FILE_WATCHED_IMDB = PATH_INPUT+'watched.imdb'     #contains only IMDB_CODE
FILE_WATCHLIST_IMDB = PATH_INPUT+'watchlist.imdb' #contains only IMDB_CODE
FOLDER_SRT_TEST = SRT_FOLDER+'test'
FOLDER_SRT_TRAIN = SRT_FOLDER+'train'

##*****--  OUTPUT --******##

FILE_WATCHED_DATA = PATH_OUTPUT+'watched.data'
FILE_WATCHLIST_DATA = PATH_OUTPUT+'watchlist.data'
FILE_TRAIN_TAG = PATH_OUTPUT+'tag_train.data'
FILE_TEST_TAG = PATH_OUTPUT+'tag_test.data'
FOLDER_TAG_TEST = TAG_FOLDER+'test'
FOLDER_TAG_TRAIN = TAG_FOLDER+'train'