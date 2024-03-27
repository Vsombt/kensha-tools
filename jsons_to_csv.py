import pandas as pd
import argparse
import os
import json
import re

def parse_args():
    parser = argparse.ArgumentParser(description='Merge Facebook messages from JSON files into a single DataFrame')
    parser.add_argument('--messages', default='data/messages_json',
                        help='Path to the directory containing JSON files')
    parser.add_argument('--group', default=None,
                        help='Name of the messenger group to use (optional)')
    return parser.parse_args()

def remove_emojis(text):
    # Unicode ranges for emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001F000-\U0001F02F"  # Mahjong Tiles
        "\U0001F0A0-\U0001F0FF"  # Playing Cards
        "\U00002600-\U000026FF"  # Miscellaneous Symbols
        "\U00002700-\U000027BF"  # Dingbats
        "\U00002B05-\U00002B07"
        "\U00002B1B-\U00002B1F"
        "\U00002B50"
        "\U00002B55"
        "]+", flags=re.UNICODE)
    
    return emoji_pattern.sub(r'', text)

def correct_encoding(text):
    try:
        return text.encode('latin1').decode('utf-8')
    except:
        return text

def remove_double_quotes(text):
    return text.replace('"', '')

def read_messages_from_file(file_path, group_name=None):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if group_name is None or data.get('title') == group_name:
            messages = data.get('messages', [])
            return [
                {
                    'group': data.get('title', 'Unknown'),
                    'sender': correct_encoding(message['sender_name']),
                    'timestamp': message['timestamp_ms'],
                    'message': remove_double_quotes(remove_emojis(correct_encoding(message.get('content', ''))))
                }
                for message in messages
            ]
    return []

def merge_messages(directory, group_name=None):
    all_messages = []
    for filename in os.listdir(directory):
        if filename.startswith('message_') and filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            all_messages.extend(read_messages_from_file(file_path, group_name))
    
    df = pd.DataFrame(all_messages)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['message'] = df['message'].apply(lambda x: x.strip())
    df = df.dropna(subset=['message'])
    df = df[df['message'] != '']
    return df

if __name__ == '__main__':
    print('Creating dataframe ...')
    args = parse_args()
    df = merge_messages(args.messages, args.group)
    print('Done!')
    print(f'Collected {len(df)} messages.')
    df.to_csv('data/messages.csv', index=False)