db.createUser({
    user: 'geo',
    pwd: 'password',
    roles: [
        {
            role: 'readWrite',
            db: 'geo_db',
        },
    ],
});
