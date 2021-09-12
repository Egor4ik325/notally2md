from pathlib import Path
from datetime import datetime

import xmltodict
from slugify import slugify


def create_notes(base_path, notes, dir_name):
    """Create notes filesystem structure."""
    notes_path = base_path / dir_name
    notes_path.mkdir()

    notes_notes = notes.get('note')
    if notes_notes:
        for i, note in enumerate(notes_notes):
            note_title = note.get('title')
            note_body = note.get('body')
            note_timestamp_created = int(note.get('date-created'))
            note_date_created = datetime.fromtimestamp(
                note_timestamp_created / 1e3)

            # Determine file name based on title or body
            if note_title:
                date_created = note_date_created.strftime(r'%Y%m%d')
                title_slug = slugify(note_title)
                filename = f'{title_slug}-{date_created}'
            elif note_body:
                body_first_line = note_body.split('\n', 1)[0]
                filename = slugify(body_first_line)

            # filename = f'note_{i}'
            note_path = notes_path / f'{filename}.md'
            with open(note_path, 'wt') as f:
                if note_title:
                    f.write(f'# {note_title }\n\n')
                if note_body:
                    f.write(note_body)

    notes_lists = notes.get('list')
    if notes_lists:
        for i, lst in enumerate(notes_lists):
            list_path = notes_path / f'list_{i}.md'
            with open(list_path, 'wt') as f:
                list_title = lst.get('title')
                if list_title:
                    f.write(f'# {list_title}\n\n')
                # Write every list item
                list_items = lst.get('item')
                if list_items:
                    for list_item in list_items:
                        if isinstance(list_item, str):
                            list_item = list_items

                        list_item_text = list_item.get('text')
                        list_item_checked = list_item.get('checked')
                        if list_item_text:
                            if list_item_checked is None:
                                f.write(f'- {list_item_text}\n')
                            elif list_item_checked.lower() == 'true':
                                f.write(f'- [x] {list_item_text}\n')
                            else:
                                f.write(f'- [ ] {list_item_text}\n')

                        if isinstance(list_item, str):
                            break


if __name__ == "__main__":
    try:
        # Read XML backup as dictionary
        with open('backup.xml') as f:
            backup = xmltodict.parse(f.read(), encoding='utf-8')
    except FileNotFoundError:
        print("Backup not found!")
    except Exception:
        print("Invalid XML structure!")
    else:
        backup_path = Path(__file__).parent

        # Try to access exported-notes node
        exported_notes = backup.get('exported-notes')
        if exported_notes is not None:
            export_path = backup_path / 'exported_notes'
            export_path.mkdir()

            notes = exported_notes.get('notes')
            if notes is not None:
                create_notes(export_path, notes, 'notes')

            # archived_notes = exported_notes.get('archived-notes')
            # if archived_notes is not None:
            #     create_notes(export_path, archived_notes, 'archived-notes')

            # deleted_notes = exported_notes.get('deleted-notes')
            # if deleted_notes is not None:
            #     create_notes(export_path, deleted_notes, 'deleted-notes')
