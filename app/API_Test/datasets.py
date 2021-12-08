test_new = [
    {"request" : { "email" : "only_test_user@getOffer.com", "password" : "test" },
     "response": "OK", "SaveTestUser": False},
    {"request" : { "email" : "getOffer7@test.com", "password" : "test" },
     "response": { "data": { "error": "user already register" }, "status": False },
     "SaveTestUser": True}
]