# Engenharia de Serviços

## Grade:
19.5/20 (only missed concurrent payment handling)

# Commands
```
./init_localstack.sh
```

# Manual Tests

- [x] Login
- [x] Register
- [x] Logout
- [x] Token expired/invalid
- [x] Book service (starting workflow)
  - [x] Dont go to the booking
  - [x] Go to the booking
    - [x] Don't pay
    - [x] Pay
      - [x] Wait for repair - admin
        - [x] Don't Pickup
        - [x] Pickup - also admin
- [x] Try to book a service at the same time as another
