#coding: UTF-8
import urllib2
import sys
import os
import math
import time
import re
from environment import *
sys.path.insert(0,os.getcwd()+'/lib')
sys.path.insert(0,os.getcwd()+'/data')
from data import *
def crawlyOscars(title_code):
	"""
		Given a imdb_code 
		return the number of oscars and nominations, and score
	"""

	movie_page	= urllib2.urlopen(title_code).readlines()
	wons = 0
	nominations = 0
	awards = False
	won = False
	nomination = False
	score = 0.0

	for index in xrange(len(movie_page)):
		line = movie_page[index]

		if 'Academy Awards, USA' in line:
			awards = True

		if '<h3>' in line:
			awards = False

		if '<b>Won</b>' in line:
			won = True
			nomination = False

		if '<b>Nominated</b>' in line:
			nomination = True
			won = False

		if '"award_description"' in line and awards:
			
			if '<br' not in movie_page[index+1]:
				continue
			award_description = movie_page[index+1].split('<br')[0].split('Best')[1]
			award_description = award_description.replace('Performance by an ','')
			award_description = award_description.replace(' of the Year','')
			award_description = award_description.replace('Achievement in ','')
			

			for O_S in OSCARS_SCORE.keys():
				if O_S in award_description:
					award_description = O_S

			if award_description not in OSCARS_SCORE:
				if won:
					wons += 1
					score += OSCARS_SCORE['Basic']
				else:
					nominations += 1
					score += OSCARS_SCORE['Basic']/4.
			else:
				if won:
					wons += 1
					score += OSCARS_SCORE[award_description]
				else:
					nominations += 1
					score += OSCARS_SCORE[award_description]/4.

	
	return {'Wons':wons,'Nominations':nominations,'Score':score}

def crawlyBAFTA(title_code):
	movie_page	= urllib2.urlopen(title_code).readlines()

	wons = 0
	bafta = False
	won = False
	score = 0.0
	for index in xrange(len(movie_page)):

		if 'BAFTA Awards' in movie_page[index]:
			bafta = True

		if bafta and '</table><br />' in movie_page[index]:
			bafta = False

		if bafta and 'Won' in movie_page[index]:
			won = True

		if won and 'Nominated' in movie_page[index]:
			won = False

		if won and bafta and 'award_description' in movie_page[index]:
			
			award = " ".join(movie_page[index+1].split('<')[0].split()[0:])
			if award in BAFTA_SCORE:
				score += BAFTA_SCORE[award]
				wons += 1



	return {'Wons':wons,'score':score}

def cralwyCANNES(title_code):
	movie_page	= urllib2.urlopen(title_code).readlines()

	wons = 0
	cannes = False
	won = False
	score = 0.0
	for index in xrange(len(movie_page)):

		if 'Cannes Film Festival' in movie_page[index]:
			cannes = True

		if cannes and "Palme d'Or<" in movie_page[index]:
			if 'Won' in movie_page[index-1]:
				wons +=1
				score += CANNES_PALME
				break

	return {'Wons':wons,'score':score}

def cralwyBerlin(title_code):
	movie_page	= urllib2.urlopen(title_code).readlines()

	wons = 0
	berlin = False
	won = False
	score = 0.0
	for index in xrange(len(movie_page)):

		if 'Berlin International Film Festival' in movie_page[index]:
			berlin = True

		if berlin and 'Golden Berlin Bear' in movie_page[index]:
			if 'Won' in movie_page[index-1]:
				wons +=1
				score += BERLIN_BEAR
				break

	return {'Wons':wons,'score':score}

def extract_movie_data(title_code):
	"""
		Given title code
		return movie_data : name,date,ranting,oscars
	"""
	
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
			if '(' not in line:
				raise Exception('The movie_IMDB %s is not registered' % title_code)
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


	oscars = crawlyOscars('http://www.imdb.com/title/%s/awards' % title_code)
	bafta = crawlyBAFTA('http://www.imdb.com/title/%s/awards' % title_code)
	berlin = cralwyBerlin('http://www.imdb.com/title/%s/awards' % title_code)
	cannes = cralwyCANNES('http://www.imdb.com/title/%s/awards' % title_code)
	
	data_line = '%s;%s;%s;' % (movie_name,movie_date,ranting)
	data_line += '%d;%d;%1.2f' % (oscars['Wons'],oscars['Nominations'],oscars['Score'])
	data_line += ';%d;%1.2f' % (bafta['Wons']+berlin['Wons']+cannes['Wons'],
							bafta['score']+berlin['score']+cannes['score'])

	for g in genres:
		data_line += ';%s' % g

	print movie_name,'Extracted'
	return {'code':title_code,'data':data_line}

def run():
	watchlist_imdb_code = open(os.getcwd()+'/'+FILE_WATCHLIST_IMDB).read().split('\n')
	watchlist_reader = open(os.getcwd()+'/'+FILE_WATCHLIST_DATA)
	watchlist_data = dict([(i.split(';')[0],";".join(i.split(';')[1:])) for i in watchlist_reader.read().split('\n')])
	watchlist_reader.close()
	

	for imdb_code in watchlist_imdb_code:
		if imdb_code not in watchlist_data:
			movie_data = extract_movie_data(imdb_code)
			watchlist_data[imdb_code] = movie_data['data']

	watchlist_data = zip(watchlist_data.values(),watchlist_data.keys())
	watchlist_data.sort()

	watchlist_writer = open(os.getcwd()+'/'+FILE_WATCHLIST_DATA,'w')
	for w in watchlist_data:
		watchlist_writer.write('%s;%s\n' % (w[1],w[0]))

run()

