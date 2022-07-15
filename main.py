from http.client import HTTPException
from fastapi import FastAPI, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from models import Query, Jira
from schemas import QuerySchema
from jira import jiraPost, jiraDelete, jiraEdit, jiraGet
import sqlalchemy as database

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@app.get("/query/all")
async def allQueries(db: Session = Depends(get_db)):
    return db.query(Query).all()


@app.get("/query/{query_id}")
async def getQuery(query_id: int, db: Session = Depends(get_db)):
    
    curr_query = db.query(Query).filter(Query.id == query_id).first()
    
    return curr_query


@app.post("/query")
async def addQuery(input_query: QuerySchema, db: Session = Depends(get_db)):

    curr_query = Query(
        query = input_query.query,
        repeats_instance = input_query.repeats_instance,
        repeats =  input_query.repeats,
        title = input_query.title,
        startTime = input_query.startTime,
        endTime = input_query.endTime,
        status = input_query.status,
        table_id = input_query.table_id,
        dataset = input_query.dataset,
        partitioning_field = input_query.partitioning_field,
        write_preference = input_query.write_preference,
        location = input_query.location,
        notify_via_mail = input_query.notify_via_mail
    )

    data = jiraPost(input_query.title, input_query.query)

    curr_jira = Jira(
        key = data["key"],
        status = input_query.status
    )

    db.add(curr_query)
    db.commit()
    db.add(curr_jira)
    db.commit()

    return data
    

@app.put("/query/{query_id}")
async def editQuery(query_id: int, input_query: QuerySchema, db: Session = Depends(get_db)):

    curr_query = db.query(Query).filter(Query.id == query_id).first()

    if curr_query is None:
        raise HTTPException(
            status_code = 404,
            detail = f"User with ID {query_id} : Does not exist"
        )
    
    curr_query.query = input_query.query
    curr_query.repeats_instance = input_query.repeats_instance
    curr_query.repeats =  input_query.repeats
    curr_query.title = input_query.title
    curr_query.startTime = input_query.startTime
    curr_query.endTime = input_query.endTime
    curr_query.status = input_query.status
    curr_query.table_id = input_query.table_id
    curr_query.dataset = input_query.dataset
    curr_query.partitioning_field = input_query.partitioning_field
    curr_query.write_preference = input_query.write_preference
    curr_query.location = input_query.location
    curr_query.notify_via_mail = input_query.notify_via_mail

    query = database.select([Jira.key]).filter(Jira.id == query_id)
    result = engine.execute(query).first()

    jiraEdit(str(result[0]), str(input_query.title), str(input_query.query))
    
    db.add(curr_query)
    db.commit()

    return input_query



@app.delete("/query/{query_id}")
async def deleteQuery(query_id: int, db: Session = Depends(get_db)):

    curr_query = db.query(Query).filter(Query.id == query_id).first()

    if curr_query is None:
        raise HTTPException(
            status_code = 404,
            detail = f"User with ID {query_id} : Does not exist"
        )

    query = database.select([Jira.key]).filter(Jira.id == query_id)
    result = engine.execute(query).first()

    jiraDelete(str(result[0]))

    db.query(Query).filter(Query.id == query_id).delete()
    db.query(Jira).filter(Jira.id == query_id).delete()

    db.commit()            

