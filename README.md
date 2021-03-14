# valorant_comp

# How to use post_match_thread.py

1. Find the desired event id by looking in the url of the vlr.gg event homepage, i.e. https://www.vlr.gg/event/120/ftw-summer-showdown
2. Run to get list of matches
```
API_TOKEN={API_TOKEN} python3 post_match_thread.py get_matchlist --event_id {event_id}
```
3. Look through output to find corresponding match_id (Note: this match_id is different from the one that appears in the url of the match on vlr.gg)
4. Run to get post match thread body (Example: https://gist.github.com/kevinluu91/67df15f95c3c74de0266520f9639df41)
```
API_TOKEN={API_TOKEN} python3 post_match_thread.py create_thread --match_id {match_id}
```
