# Problem #7
The problem is the client creates a session on the webserver. The webserver has 2 components Server A and B.Server A have processing delay mean 10 seconds (exponential distributed) and Server B have processing delay mean 15 seconds (exponential distributed). If total times more than 40 seconds the system will raise system timeout error. The goal of this simulation needs to find the average time of this model and the probability that it timed out.

```sequence
 Client <- wait for 40s -> [ Server A (avg 10s expo) -> Server B (avg 15s expo) ]
```

## Question
1. Average processing time ?
`Average processing time is 25.00293038 seconds`
   
2. The probability that timed out ?
`Timeout probability is 0.17183520 (17.18352 %)`
