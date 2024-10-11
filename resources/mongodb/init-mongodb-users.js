db = db.getSiblingDB('admin')

db.runCommand({
    createRole: "listDatabases",
    privileges: [
        { resource: { cluster : true }, actions: ["listDatabases"]}
    ],
    roles: []
});

db.runCommand({
    createRole: "readChangeStream",
    privileges: [
        { resource: { db: "", collection: ""}, actions: [ "find", "changeStream" ] }
    ],
    roles: []
});

db.createUser({
    user: 'debezium',
    pwd: 'dbz',
    roles: [
        { role: "readWrite", db: "inventory" },
        { role: "readChangeStream", db: "admin" },
        { role: "readAnyDatabase", db: "admin" },
        { role: "read", db: "local" },
        { role: "read", db: "config" }
    ]
});
