#!/usr/bin/env python3
"""
Supabase Data Manipulation Tool
For authorized bug bounty and penetration testing use only
"""

import argparse
import requests
import json
import sys
from typing import Dict, List, Optional
from urllib.parse import urljoin

class SupabaseDataTool:
    def __init__(self, url: str, api_key: str, auth_token: Optional[str] = None):
        self.base_url = url.rstrip('/')
        self.api_key = api_key
        self.auth_token = auth_token
        self.headers = {
            'apikey': api_key,
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
        if auth_token:
            self.headers['Authorization'] = f'Bearer {auth_token}'
    
    def print_banner(self):
        banner = r"""
 ███████╗██╗   ██╗██████╗  █████╗ ███╗   ███╗ █████╗ ██████╗ 
 ██╔════╝██║   ██║██╔══██╗██╔══██╗████╗ ████║██╔══██╗██╔══██╗
 ███████╗██║   ██║██████╔╝███████║██╔████╔██║███████║██████╔╝
 ╚════██║██║   ██║██╔═══╝ ██╔══██║██║╚██╔╝██║██╔══██║██╔═══╝
 ███████║╚██████╔╝██║     ██║  ██║██║ ╚═╝ ██║██║  ██║██║     
 ╚══════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     
                                                               
      [ Supabase Data Extraction & Manipulation Framework ]
               [ For Authorized Security Testing ]
        """
        print(banner)
        print("=" * 70)
        print(f"  Target      : {self.base_url}")
        print(f"  Author      : dnlalb.exe")
        print(f"  Version     : 1.0")
        print("=" * 70 + "\n")
    
    def list_tables(self) -> List[str]:
        """List all available tables"""
        print("[*] Listing available tables...")
        tables = []
        try:
            response = requests.get(
                f"{self.base_url}/rest/v1/",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'definitions' in data:
                    tables = list(data['definitions'].keys())
                elif 'paths' in data:
                    tables = [path.strip('/') for path in data['paths'].keys()]
            
            if tables:
                print(f"[+] {len(tables)} table(s) found:\n")
                for i, table in enumerate(tables, 1):
                    print(f"    {i}. {table}")
            else:
                print("[-] No tables found or access denied")
            
            print()
            return tables
            
        except Exception as e:
            print(f"[-] Error listing tables: {str(e)}\n")
            return []
    
    def list_all_records(self, table: str, limit: int = 1000, offset: int = 0, 
                         filters: Optional[Dict] = None, order_by: Optional[str] = None) -> Optional[List[Dict]]:
        """List all records from a table"""
        print(f"[*] Listing records from table '{table}'...")
        try:
            params = {'limit': limit, 'offset': offset}
            
            # Add filters if provided
            if filters:
                for key, value in filters.items():
                    params[key] = f"eq.{value}"
            
            # Add ordering if provided
            if order_by:
                params['order'] = order_by
            
            response = requests.get(
                f"{self.base_url}/rest/v1/{table}",
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"[+] {len(data)} record(s) found\n")
                
                # Display data in formatted way
                if data:
                    print(json.dumps(data, indent=2, ensure_ascii=False))
                    print()
                
                return data
            else:
                print(f"[-] Failed to list records. Status: {response.status_code}")
                print(f"    Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"[-] Error listing records: {str(e)}")
            return None
    
    def query_records(self, table: str, filters: Dict, limit: int = 100) -> Optional[List[Dict]]:
        """Query records with specific filters"""
        print(f"[*] Querying records in table '{table}' with filters...")
        try:
            # Build query string with filters
            query_params = []
            for key, value in filters.items():
                query_params.append(f"{key}=eq.{value}")
            
            query_string = "&".join(query_params)
            url = f"{self.base_url}/rest/v1/{table}?{query_string}&limit={limit}"
            
            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"[+] {len(data)} record(s) found\n")
                
                if data:
                    print(json.dumps(data, indent=2, ensure_ascii=False))
                    print()
                
                return data
            else:
                print(f"[-] Query failed. Status: {response.status_code}")
                print(f"    Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"[-] Error during query: {str(e)}")
            return None
    
    def insert_record(self, table: str, data: Dict) -> Optional[Dict]:
        """Insert a new record"""
        print(f"[*] Inserting record into table '{table}'...")
        try:
            response = requests.post(
                f"{self.base_url}/rest/v1/{table}",
                headers=self.headers,
                json=data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                result = response.json() if response.text else data
                print(f"[+] Record inserted successfully!\n")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                print()
                return result
            else:
                print(f"[-] Insert failed. Status: {response.status_code}")
                print(f"    Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"[-] Error during insert: {str(e)}")
            return None
    
    def update_records(self, table: str, filters: Dict, data: Dict) -> bool:
        """Update existing records"""
        print(f"[*] Updating records in table '{table}'...")
        try:
            # Build query string with filters
            query_params = []
            for key, value in filters.items():
                query_params.append(f"{key}=eq.{value}")
            
            query_string = "&".join(query_params)
            url = f"{self.base_url}/rest/v1/{table}?{query_string}"
            
            response = requests.patch(
                url,
                headers=self.headers,
                json=data,
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                print(f"[+] Record(s) updated successfully!")
                if response.text:
                    result = response.json()
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                print()
                return True
            else:
                print(f"[-] Update failed. Status: {response.status_code}")
                print(f"    Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"[-] Error during update: {str(e)}")
            return False
    
    def delete_records(self, table: str, filters: Dict) -> bool:
        """Delete records"""
        print(f"[*] Deleting records from table '{table}'...")
        try:
            # Build query string with filters
            query_params = []
            for key, value in filters.items():
                query_params.append(f"{key}=eq.{value}")
            
            query_string = "&".join(query_params)
            url = f"{self.base_url}/rest/v1/{table}?{query_string}"
            
            response = requests.delete(
                url,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                print(f"[+] Record(s) deleted successfully!")
                if response.text:
                    result = response.json()
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                print()
                return True
            else:
                print(f"[-] Delete failed. Status: {response.status_code}")
                print(f"    Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"[-] Error during delete: {str(e)}")
            return False
    
    def export_table(self, table: str, filename: str, limit: int = 10000) -> bool:
        """Export all data from a table to JSON file"""
        print(f"[*] Exporting table '{table}' to {filename}...")
        
        all_data = []
        offset = 0
        batch_size = 1000
        
        while True:
            try:
                response = requests.get(
                    f"{self.base_url}/rest/v1/{table}",
                    headers=self.headers,
                    params={'limit': batch_size, 'offset': offset},
                    timeout=10
                )
                
                if response.status_code == 200:
                    batch = response.json()
                    if not batch:
                        break
                    
                    all_data.extend(batch)
                    offset += batch_size
                    print(f"    Downloaded {len(all_data)} records...")
                    
                    if len(all_data) >= limit:
                        break
                else:
                    print(f"[-] Export failed. Status: {response.status_code}")
                    return False
                    
            except Exception as e:
                print(f"[-] Error during export: {str(e)}")
                return False
        
        # Save to file
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2, ensure_ascii=False)
            print(f"[+] {len(all_data)} records exported successfully!\n")
            return True
        except Exception as e:
            print(f"[-] Error saving file: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description='Supabase Data Manipulation Tool - For authorized use',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Usage examples:

  # List tables
  %(prog)s -u https://xxx.supabase.co -k KEY list-tables

  # List all records from a table
  %(prog)s -u https://xxx.supabase.co -k KEY list -t users

  # Query with filters
  %(prog)s -u https://xxx.supabase.co -k KEY query -t users -f '{"email":"test@example.com"}'

  # Insert record
  %(prog)s -u https://xxx.supabase.co -k KEY insert -t users -d '{"name":"John","email":"john@example.com"}'

  # Update records
  %(prog)s -u https://xxx.supabase.co -k KEY update -t users -f '{"id":"123"}' -d '{"name":"Jane"}'

  # Delete records
  %(prog)s -u https://xxx.supabase.co -k KEY delete -t users -f '{"id":"123"}'

  # Export entire table
  %(prog)s -u https://xxx.supabase.co -k KEY export -t users -o users.json
        '''
    )
    
    parser.add_argument('-u', '--url', required=True, help='Supabase URL')
    parser.add_argument('-k', '--apikey', required=True, help='API Key')
    parser.add_argument('-a', '--auth', help='Authorization token (optional)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Command list-tables
    subparsers.add_parser('list-tables', help='List all tables')
    
    # Command list
    list_parser = subparsers.add_parser('list', help='List records from a table')
    list_parser.add_argument('-t', '--table', required=True, help='Table name')
    list_parser.add_argument('-l', '--limit', type=int, default=100, help='Record limit')
    list_parser.add_argument('--offset', type=int, default=0, help='Offset')
    list_parser.add_argument('--order', help='Order by (ex: created_at.desc)')
    
    # Command query
    query_parser = subparsers.add_parser('query', help='Query records with filters')
    query_parser.add_argument('-t', '--table', required=True, help='Table name')
    query_parser.add_argument('-f', '--filters', required=True, help='Filters in JSON (ex: {"id":"123"})')
    query_parser.add_argument('-l', '--limit', type=int, default=100, help='Record limit')
    
    # Command insert
    insert_parser = subparsers.add_parser('insert', help='Insert a new record')
    insert_parser.add_argument('-t', '--table', required=True, help='Table name')
    insert_parser.add_argument('-d', '--data', required=True, help='Data in JSON format')
    
    # Command update
    update_parser = subparsers.add_parser('update', help='Update records')
    update_parser.add_argument('-t', '--table', required=True, help='Table name')
    update_parser.add_argument('-f', '--filters', required=True, help='Filters in JSON format')
    update_parser.add_argument('-d', '--data', required=True, help='Data to update in JSON format')
    
    # Command delete
    delete_parser = subparsers.add_parser('delete', help='Delete records')
    delete_parser.add_argument('-t', '--table', required=True, help='Table name')
    delete_parser.add_argument('-f', '--filters', required=True, help='Filters in JSON format')
    
    # Command export
    export_parser = subparsers.add_parser('export', help='Export entire table')
    export_parser.add_argument('-t', '--table', required=True, help='Table name')
    export_parser.add_argument('-o', '--output', required=True, help='Output file')
    export_parser.add_argument('-l', '--limit', type=int, default=10000, help='Maximum limit')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize the tool
    tool = SupabaseDataTool(args.url, args.apikey, args.auth)
    tool.print_banner()
    
    # Execute command
    try:
        if args.command == 'list-tables':
            tool.list_tables()
        
        elif args.command == 'list':
            tool.list_all_records(args.table, args.limit, args.offset, order_by=args.order)
        
        elif args.command == 'query':
            filters = json.loads(args.filters)
            tool.query_records(args.table, filters, args.limit)
        
        elif args.command == 'insert':
            data = json.loads(args.data)
            tool.insert_record(args.table, data)
        
        elif args.command == 'update':
            filters = json.loads(args.filters)
            data = json.loads(args.data)
            tool.update_records(args.table, filters, data)
        
        elif args.command == 'delete':
            filters = json.loads(args.filters)
            
            # Confirmation before deleting
            print(f"[!] WARNING: You are about to delete records from table '{args.table}'")
            print(f"    Filters: {filters}")
            confirm = input("    Type 'YES' to confirm: ")
            
            if confirm == 'YES':
                tool.delete_records(args.table, filters)
            else:
                print("[-] Operation cancelled.")
        
        elif args.command == 'export':
            tool.export_table(args.table, args.output, args.limit)
    
    except json.JSONDecodeError:
        print("[-] Error: Invalid JSON in parameters")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()