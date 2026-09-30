"""Handles library member registration."""

from db_init import read_data, write_data, get_next_id
from config import MEMBERS_FILE

def register_new_member():
    members = read_data(MEMBERS_FILE)
    
    print("\n----- Register New Member -----")
    full_name = input('Enter Full Name: ').strip()
    department_class = input('Enter Class/Department: ').strip()
    phone_contact = input('Enter Contact Number: ').strip()
    
    new_member = {
        'member_id': get_next_id(members, 'member_id'),
        'name': full_name,
        'class': department_class,
        'contact': phone_contact
    }
    
    members.append(new_member)
    write_data(MEMBERS_FILE, list(new_member.keys()), members)
    print(f"[+] Member '{full_name}' successfully registered.")