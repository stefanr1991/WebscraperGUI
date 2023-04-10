import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import requests
import webbrowser

# window
window = tk.Tk()
window.title('webscraper')
window.geometry('800x600')

# title
title_label = ttk.Label(master=window, text='Hackernews', font='calibri 24 bold')
title_label.place(relx=0.5, rely=0.1, anchor='center')

# label frame to hold the treeview widget
frame = ttk.LabelFrame(window, text="Output")
frame.place(relx=0.5, rely=0.5, anchor='center')


# treeview widget
treeview = ttk.Treeview(frame, columns=('Title', 'Link', 'Votes'), show='headings')
treeview.heading('Title', text='Title')
treeview.heading('Link', text='Link')
treeview.heading('Votes', text='Votes')
treeview.pack()


# sorts the stories by votes
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        if links[idx].find('a'):
            href = links[idx].find('a')['href']
        else:
            href = None
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)

def create_table():
    urls = ['https://news.ycombinator.com/news', 'https://news.ycombinator.com/news?p=2', 'https://news.ycombinator.com/news?p=3']
    results = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select('.titleline')
        subtext = soup.select('.subtext')
        results += create_custom_hn(links, subtext)

    # Delete existing items before inserting new ones
    treeview.delete(*treeview.get_children())

    for item in results:
        treeview.insert('', 'end', values=(item['title'], item['link'], item['votes']))


# double click to open links
def open_link(event):
    item = treeview.selection()[0]
    link = treeview.item(item)['values'][1]
    if link:
        webbrowser.open(link)

treeview.bind("<Double-1>", open_link)

# button that takes the function of the web scraper
button = ttk.Button(master=window, text="Start scraping", command=create_table)
button.place(relx=0.5, rely=0.2, anchor='center')

# run
window.mainloop()
