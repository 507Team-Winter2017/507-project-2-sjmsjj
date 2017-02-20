#proj2.py
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_soup(url):
	req = Request(url, None, {'User-Agent': 'SI_CLASS'})
	html = urlopen(req)
	# html = urlopen(url, context=ctx).read()
	soup = BeautifulSoup(html, "html.parser")
	return soup

def get_tags(soup, tag_name, css_class=''):
	if css_class:
		return soup.find_all(tag_name, class_=css_class)
	return soup(tag_name)


#### Problem 1 ####
def do_problem1():
	url = "http://nytimes.com"
	soup = get_soup(url)
	tags = get_tags(soup, "h2", "story-heading")[:10]	
	print('\n*********** PROBLEM 1 ***********')
	print('New York Times -- First 10 Story Headings\n')
	for tag in tags:
		print(tag.get_text().strip())

### Your Problem 1 solution goes here


#### Problem 2 ####
def do_problem2():
	url = "https://www.michigandaily.com/"
	soup = get_soup(url)
	tag = get_tags(soup, "div", "pane-mostread")[0]
	sub_tags = tag.find_all("li")
	print('\n*********** PROBLEM 2 ***********')
	print('Michigan Daily -- MOST READ\n')
	for sub_tag in sub_tags:
		print(sub_tag.get_text().strip())

# ### Your Problem 2 solution goes here


# #### Problem 3 ####
def do_problem3():
	url = "http://newmantaylor.com/gallery.html"
	soup = get_soup(url)
	tags = get_tags(soup, "img")
	print('\n*********** PROBLEM 3 ***********')
	print("Mark's page -- Alt tags\n")
	for tag in tags:
		alt_text = tag.get("alt", None)
		if alt_text is not None:
			print(alt_text)
		else:
			print("No alternative text provided!!")

# ### Your Problem 3 solution goes here


# #### Problem 4 ####
base_url = "https://www.si.umich.edu"
def extract_email(short_url):
	url = base_url + short_url
	soup = get_soup(url)
	email = soup.find('a', href=re.compile(r'.+@.+')).get_text().strip()
	return email

def print_emails(url, index=1):
	soup = get_soup(url)
	tags = soup.find_all('a', string='Contact Details')
	for tag in tags:
		short_url = tag.get('href', '').strip()
		email = extract_email(short_url)
		print(str(index) + " " + email)
		index += 1
	tag = soup.find('a', title='Go to next page')
	if tag is not None:
		next_page = tag.get('href', '').strip()
		print_emails(base_url + next_page, index)

def do_problem4():
	print('\n*********** PROBLEM 4 ***********')
	print("UMSI faculty directory emails\n")
	url = "https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4"
	print_emails(url)

### Your Problem 4 solution goes here

def main():
	do_problem1()
	do_problem2()
	do_problem3()
	do_problem4()

if __name__ == '__main__':
	main()