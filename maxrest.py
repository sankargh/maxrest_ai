import sqlite3
import pandas as pd
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import uvicorn
from person import Person
from asset import Asset
from location import Location

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure the SQLite DB and table exist before the app starts
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
# ---------- SQLite BACKING (maximo.db) ----------
DB_FILE = "database/maximo.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create the person, asset, and Locations tables in maximo.db if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS person (
            personid INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )
        """
    )

    # Create asset table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS asset (
            assetuid INTEGER PRIMARY KEY,
            assetnum TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT NOT NULL,
            siteid TEXT NOT NULL
        )
        """
    )

    # Create Locations table (for Location records)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Locations (
            locationuid INTEGER PRIMARY KEY,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            siteid TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()

# ---------- ROUTES ----------
@app.get("/")
def read_root():
    return "<html><p>Welcome to my page</p></html>"

@app.post("/maxrest/rest/mbo/person")
def add_person(person: Person):
    """Add a Person record into maximo.db."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO person (personid, name, age, email)
            VALUES (?, ?, ?, ?)
            """,
            (person.personid, person.name, person.age, person.email),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Person with this personid already exists",
        )

    conn.close()
    return {"status": "ok", "source": "db", "message": "Person added to database"}


@app.get("/maxrest/rest/mbo/person")
def get_all_persons():
    """Get all Person records from maximo.db."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT personid, name, age, email FROM person")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/maxrest/rest/mbo/person/{personid}")
def get_person(personid: int):
    """Get a single Person record from maximo.db by personid."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT personid, name, age, email FROM person WHERE personid = ?",
        (personid,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Person not found in database")

    return dict(row)


@app.post("/maxrest/rest/mbo/asset")
def add_asset(asset: Asset):
    """Add an Asset record into maximo.db."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO asset (assetuid, assetnum, description, location, siteid)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                asset.assetuid,
                asset.assetnum,
                asset.description,
                asset.location,
                asset.siteid,
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Asset with this assetuid already exists",
        )

    conn.close()
    return {"status": "ok", "source": "db", "message": "Asset added to database"}


@app.get("/maxrest/rest/mbo/asset")
def get_all_assets():
    """Get all Asset records from maximo.db."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT assetuid, assetnum, description, location, siteid FROM asset"
    )
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/maxrest/rest/mbo/asset/{asset}")
def get_asset(asset: str):
    """Get a single Asset record from maximo.db by assetnum."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT assetuid, assetnum, description, location, siteid FROM asset WHERE assetuid = ?",
        (asset,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Asset not found in database")

    return dict(row)


@app.post("/maxrest/rest/mbo/location")
def add_location(location: Location):
    """Add a Location record into maximo.db (Locations table)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Locations (locationuid, location, description, siteid)
            VALUES (?, ?, ?, ?)
            """,
            (
                location.locationuid,
                location.location,
                location.description,
                location.siteid,
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Location with this locationuid already exists",
        )

    conn.close()
    return {"status": "ok", "source": "db", "message": "Location added to database"}


@app.get("/maxrest/rest/mbo/location")
def get_all_locations():
    """Get all Location records from maximo.db (Locations table)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT locationuid, location, description, siteid FROM Locations"
    )
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/maxrest/rest/mbo/location/{location}")
def get_location(location: str):
    """Get a single Location record from maximo.db by location (Locations table)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT locationuid, location, description, siteid FROM Locations WHERE locationuid = ?",
        (location,),
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Location not found in database")

    return dict(row)


if __name__ == "__main__":
    uvicorn.run("maxrest:app", host="127.0.0.1", port=5000, reload=True)