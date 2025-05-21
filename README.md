# Engenharia de Serviços

# TODO
- FIX FRONTEND (se tiver tempo)

- Button to delete the booking (admin only) ?

- Test everything (manually)

- !!! Try to deploy it to AWS !!!


- indepotent payment ? SERIALIZE - idk if this is done

# Commands
```
./init_localstack.sh
```

# Tests

- [x] Login
- [x] Register
- [x] Logout
- [x] Token expired/invalid
- [ ] Book service (starting workflow)
  - [ ] Dont go to the booking
  - [ ] Go to the booking
    - [ ] Don't pay
    - [ ] Pay
      - [ ] Wait for repair - admin
        - [ ] Don't Pickup
        - [ ] Pickup - also admin
- [ ] Try to book a service at the same time as another