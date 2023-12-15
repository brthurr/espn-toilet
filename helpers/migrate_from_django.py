import json
from flask import current_app

def import_owners(file_path, db, Owner):
    with open(file_path, 'r') as file:
        owners_data = json.load(file)
    
    for owner_data in owners_data:
        sid = owner_data['fields']['sid']
        owner_name = owner_data['fields']['name']
        owner = Owner.query.filter_by(espn_id=sid).first()
        if owner is None:
            new_owner = Owner(
                espn_id=owner_data['fields']['sid'],
                name=owner_data['fields']['name'],
                email=owner_data['fields']['email'],
                phone=owner_data['fields']['phone']
                )
            db.session.add(new_owner)
            current_app.logger.info(f"{new_owner.name} added.")
        else:
            current_app.logger.warning(f"{owner_name} already exists. Skipping...")
    db.session.commit()


