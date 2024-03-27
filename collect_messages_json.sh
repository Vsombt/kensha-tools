#!/bin/bash

# Script to find and copy JSON files containing 'message' in their names from data/raw_facebook_data to data/messages_json

find data/raw_facebook_data -type f -name "*message_*.json" | while read file; do
  cp "$file" data/messages_json/;
done