CREATE TABLE quotes (
    quote_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    quote_text TEXT NOT NULL,
    created_on DATE NOT NULL DEFAULT CURRENT_DATE,

    CONSTRAINT quotes_quote_text_not_blank CHECK (length(btrim(quote_text)) > 0),
    CONSTRAINT quotes_quote_text_normalized CHECK (quote_text = btrim(quote_text))
);

CREATE UNIQUE INDEX quotes_quote_text_key ON quotes (lower(quote_text)); -- this would allow for unique quotes and keep the capitalization of the quotes added

CREATE TABLE tags (
    tag_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tag_name TEXT NOT NULL,

    CONSTRAINT tags_tag_name_valid CHECK (
        tag_name = btrim(tag_name) -- we are forcing tags to have no extra spacing on the outside
        AND length(tag_name) BETWEEN 1 AND 50
    )
);

CREATE UNIQUE INDEX tags_tag_name_key ON tags (lower(tag_name)); --allows for unqiue quotes and keeps the capitalization of the tags

CREATE TABLE quote_tags (
    quote_id INT NOT NULL,
    tag_id INT NOT NULL,
    CONSTRAINT quote_tags_pkey PRIMARY KEY (quote_id, tag_id),
    CONSTRAINT quote_tags_quote_id_fkey FOREIGN KEY (quote_id)
        REFERENCES quotes (quote_id) ON DELETE CASCADE, -- this deletes all pairs of quote_id, tag_id in this child table that references a quote_id that was deleted
    CONSTRAINT quote_tags_tag_id_fkey FOREIGN KEY (tag_id)
        REFERENCES tags (tag_id) ON DELETE RESTRICT -- restrict means postgres wont allow the deletion of a tag that is still referenced by a quote in this table
);