
# points-exercise

points-exercise is a web service that creates a log of point accumulation transactions consisting of a payer, point total, and timestamp, allows for the spending of said points, and reports point totals by payer.


## Installation

If you don't have it already, you'll need to install Docker. You can find the instructions to do so here: https://docs.docker.com/get-docker/

After docker has been installed, pull this repo and navigate to it on your machine using terminal, command prompt, etc. Once there, run these commands:

```bash
  docker build -t points .
  docker run -p 5000:5000 points
```
This will run a docker container containing the points-exercise service. You can then make requests to the endpoints indicated below.
## Endpoints

The base URL for all requests when being made to the docker container is:
```
http://localhost:5000
```
<details>
<summary> Add transaction</summary>

#### **Add transaction**

```http
  POST /add
```
Adds a transaction for a specific payer. Responds with a copy of the transaction that was added.  

Structure:  
```
{
  "payer": <string>
  "points": <integer>
  "timestamp": <date>
}
```
Example:  
```
{
  "payer": "Let's Potato Chips"
  "points": 5000
  "timestamp": "2020-09-04T12:30:00Z"
}
```
</details>

<details>
<summary> Spend points</summary>

#### **Spend points**

```
  POST /spend
```
Spends a requested amount of points. Points from the oldest (by timestamp) transactions will be spent first. Responds with a list of all total points spent by each payer.  

Structure:
```
{
  points: <integer>
}
```
Example:
```
{
  points: 2000
}
```
</details>

<details>
<summary>Get balances</summary>

#### **Get balances**

```
  GET /balances
```
Responds with a list of individual balances for each payer.
</details>