#coding: UTF-8
import urllib2
import sys
import os
import math
import time
from config import *
sys.path.insert(0,os.getcwd()+'/lib')
from utils import *

def crawlyOscars(title_code):

	movie_page	= urllib2.urlopen(title_code).readlines()
	wons = 0
	nominations = 0
	awards = False
	won = False
	nominations = False
	score = 0.0

	for index in xrange(len(movie_page)):
		line = movie_page[index]

		if 'Academy Awards, USA' in line:
			awards = True

		if '<h3>' in line:
			awards = False

		if '<b>Won</b>' in line:
			won = True
			nominations = False

		if '<b>Nominated</b>' in line:
			nominations = True
			won = False

		if '"award_description"' in line and awards:
			#print "#%s#" % movie_page[index+1]
			if '<br' not in movie_page[index+1]:
				continue
			award_description = movie_page[index+1].split('<br')[0].split('Best')[1]

			for O_S in OSCARS_SCORE.keys():
				if O_S in award_description:
					award_description = O_S

			if award_description not in OSCARS_SCORE:
				if won:
					wons += 1
					score += OSCARS_SCORE['Basic']
				else:
					nominations += 1
					score += OSCARS_SCORE['Basic']/3.
			else:
				if won:
					wons += 1
					score += OSCARS_SCORE[award_description]
				else:
					nominations += 1
					score += OSCARS_SCORE[award_description]/3.

				

			#print '#%s#' % award_description


	return {'Wons':wons,'Nominations':nominations,'Score':score}

def extract_movie_data(title_code):
	oscars = crawlyOscars('http://www.imdb.com/title/%s/awards' % title_code)
	movie_page	= urllib2.urlopen('http://www.imdb.com/title/%s' % title_code).readlines()
	ranting = None
	movie_name = None
	movie_date = None
	genres = []


	for index in xrange(0,1500):

		line = movie_page[index]

		if '<div class="ratingValue">' in line:
			ranting = movie_page[index+1].split('<strong title="')[1].split(' based on ')[0]

		if "<meta property='og:title' " in line:
			movie_name = line.split('content="')[1].split('" />')[0]
			movie_date = movie_name.split(' (')[1].split(')')[0]
			movie_name = movie_name.split(' (')[0]
			movie_name = movie_name.replace(' ','_')
			movie_name = movie_name.replace('__','_')
			movie_name = movie_name.lower()
			movie_name = movie_name.replace(':','_')
			movie_name = movie_name.replace('.','_')
			movie_name = movie_name.replace(',','_')
			movie_name = movie_name.replace('-','_')
			movie_name = movie_name.replace('(','_')
			movie_name = movie_name.replace(')','_')
			movie_name = movie_name.replace("'",'_')
			movie_name = movie_name.replace('"','_')
			movie_name = movie_name.replace('__','_')


		if 'op" itemprop="genre">' in line:
			genres.append(line.split('op" itemprop="genre">')[1].split('</')[0])

	
	data_line = '%s;%s;%s;' % (movie_name,movie_date,ranting)
	data_line += '%d;%d;%d' % (oscars['Wons'],oscars['Nominations'],oscars['Score'])

	for g in genres:
		data_line += ';%s' % g

	print movie_name,'Extracted'
	return {'code':title_code,'data':data_line}

def run():
	movies_title_code = open(os.getcwd()+'/'+PATH__NEW_MOVIES_CODE).read().split('\n')
	new_movies_stored = open(os.getcwd()+'/'+PATH__NEW_MOVIES)
	watched_movies    = open(os.getcwd()+'/'+PATH__WATCHED_MOVIES).read().split('\n')
	movies_stored_data = new_movies_stored.read().split('\n')[0:-1]
	

	new_movies_date   = dict([ (m.split(';')[0],int(m.split(';')[2])) for m in movies_stored_data])
	new_movies_buffer = dict([ (m.split(';')[0],";".join(m.split(';')[1:])) for m in movies_stored_data])
	new_movies_stored.close()
	watched_movies_code = [ m.split(';')[0] for m in watched_movies]
	
	for movie_code in movies_title_code:
		movie_data_extracted = None

		if movie_code in watched_movies:
			raise Exception('The movie % is in both watched and new files' % movie_code)

		elif movie_code not in new_movies_date: #or (movie_code in new_movies_date and new_movies_date[movie_code] >= time.gmtime().tm_year-1):
			movie_data_extracted = extract_movie_data(movie_code)
			new_movies_buffer[movie_data_extracted['code']] = movie_data_extracted['data']
			

		elif movie_code not in new_movies_date and movie_data_extracted == None:
			raise Exception('The movie %s was not extracted' % movie_code)

	new_movies_writer = open(os.getcwd()+'/'+PATH__NEW_MOVIES,'w')

	new_movies_buffer = zip(new_movies_buffer.values(),new_movies_buffer.keys())
	new_movies_buffer.sort()
	
	for line in new_movies_buffer:
		new_movies_writer.write('%s;%s\n' % (line[1],line[0]))