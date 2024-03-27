import pandas as pd
import argparse
import os
import json

def parse_args():
    parser = argparse.ArgumentParser(description='Merge Facebook messages from JSON files into a single DataFrame')
    parser.add_argument('--messages', default='data/messages_json',
                        help='Path to the directory containing JSON files')
    parser.add_argument('--group', default=None,
                        help='Name of the messenger group to use (optional)')
    return parser.parse_args()

def read_messages_from_file(file_path, group_name=None):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if group_name is None or data.get('title') == group_name:
            messages = data.get('messages', [])
            return [
                {
                    'group': data.get('title', 'Unknown'),
                    'sender': message['sender_name'],
                    'timestamp': message['timestamp_ms'],
                    'message': message.get('content', '')
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
    return df

if __name__ == '__main__':
    print('Creating dataframe ...')
    args = parse_args()
    df = merge_messages(args.messages, args.group)
    print('Done!')
    print(f'Collected {len(df)} messages.')
    df.to_csv('data/messages.csv')