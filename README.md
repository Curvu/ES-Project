# Engenharia de Serviços

# TODO
- [ ] Urgent: criar toasty para alertas
- [ ] MY BOOKINGS PAGE

# Duvidas
- schedule automatico update? SIM


- Suposto usar workflow para oq exatamente?
  - tipo, sø para o booking ou tambem para obter coisas da DB? (para mim nao faz sentido)

- workflow:
  - user books service 
  - workflows waits for the schedule run-out or admin change the state of it
  - user goes to schedule? (toggle in admin panel)
    - if yes, go to payment
    - if no, finish


dynamodb:
- só o estado do workflow


- can_book é suposto bloquear quando? quando o user já tem um schedule que nao foi acabado?
- podemos usar bibliotecas para frontend?

# Commands
creating lambda function locally:
```
zip function.zip function_name.py
```
```
aws --endpoint-url=http://localhost:4566 lambda create-function \
  --function-name function_name \
  --runtime python3.8 \
  --role arn:aws:iam::000000000000:role/service-role-for-lambda \
  --handler function_name.lambda_handler \
  --zip-file fileb://function.zip
```

creating step function locally:
```
aws --endpoint-url=http://localhost:4566 stepfunctions create-state-machine \
  --name "BookingWorkflow" \
  --definition file://booking.json \
  --role-arn arn:aws:iam::000000000000:role/StepFunctionsExecutionRole
```
