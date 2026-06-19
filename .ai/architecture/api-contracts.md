# API Contracts

Base URL

/api/v1

---

# Health

GET /health

Response

200 OK

{
"status": "healthy"
}

---

# Exercises

GET /exercises

Query Params

page
limit
search
muscle_group
movement_group
equipment

Response

200 OK

{
"items": [],
"page": 1,
"limit": 20,
"total": 100
}

---

GET /exercises/{id}

Response

200 OK

{
"id": "",
"name": "",
"description": "",
"instructions": [],
"equipments": [],
"alternatives": []
}

---

POST /exercises

Create Exercise

Admin Only (future)

---

PUT /exercises/{id}

Update Exercise

Admin Only (future)

---

DELETE /exercises/{id}

Soft Delete

Admin Only (future)

---

# Exercise Alternatives

GET /exercises/{id}/alternatives

Response

200 OK

[
{
"id": "",
"name": ""
}
]

---

# Muscle Groups

GET /muscle-groups

Response

200 OK

[]

---

POST /muscle-groups

Future Admin

---

PUT /muscle-groups/{id}

Future Admin

---

DELETE /muscle-groups/{id}

Future Admin

---

# Movement Groups

GET /movement-groups

Response

200 OK

[]

---

# Equipments

GET /equipments

Response

200 OK

[]

---

# Catalog

GET /catalog/version

Response

{
"version": 15,
"checksum": "hash"
}

---

GET /catalog/sync

Query Params

current_version

Response

{
"version": 16,
"changes": []
}
