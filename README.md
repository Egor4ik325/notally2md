# Notally XML backup to Markdown converter

This program converts Notally backup *XML structure* into similar *filesystem structure*. Basically it recreates note files from backup file.


## Development plan

1. Convert XML backup to dict/json representation.
2. Check & create filesystem structure.


## Backup XML document structure

```xml
<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<exported-notes>
    <notes>
        <note>
            <date-created>...</date-created>
            <pinned>...</pinned>
            <title>...</title>
            <body>...</body>
        </note>
        <list>
            <date-created>...</date-created>
            <pinned>...</pinned>
            <title>...</title>
            <item>
                <text>...</text>
                <checked>...</checked>
            </item>
            ...
        </list>
    </notes>
    <archived-notes>
        ...
    <archived-notes>
    <deleted-notes>
        ...
    <deleted-notes>
</exported-notes>
```

## Filesystem structure

