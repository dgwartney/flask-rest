# Example Python REST API Using Flask

This Flask application is provides the ability to list a set of shoe products or search for given product using the product id.

## Prerequisites

- VM, PC, or latop to run
- Python 3.6 environment with Flask package
- ngrok [here](https://ngrok.com/)


## Setup 

1. Clone [https://github.com/dgwartney/kore-rest](https://github.com/dgwartney/kore-rest) from github.
2. Configure a Python environment (virtual environment using venv or conda your choice) with flask package
3. Use ngrok to provide a routeable end-point
4. Source the `env.sh` file to set environment variables
5. Run the command `flask run`

## Provided APIs

### List Products

Lists all of the products.

### GET

````
$ curl 'http://localhost:5000/products' -H 'accept: application/json' 
````

```json
{
  "products": [
    {
      "URL": "https://www.nike.com/in/t/air-force-1-07-essential-shoe-BHN3Db/CJ1646-600",
      "Product Name": "Nike Air Force 1 '07 Essential",
      "Product ID": "CJ1646-600",
      "Listing Price": false,
      "Sale Price": 7495,
      "Discount": false,
      "Brand": "Nike",
      "Description": "Let your shoe game shimmer in the Nike Air Force 1 '07 Essential. It takes the classic AF-1 design to the next level with its premium leather upper and iridescent Swoosh.",
      "Rating": 0,
      "Reviews": 0,
      "Images": [
        "https://static.nike.com/a/images/t_PDP_1728_v1/20488f52-3686-476c-b4b8-0ca430c34a05/air-force-1-07-essential-shoe-BHN3Db.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/e9fe72b4-a153-4019-8ea6-9f31230b247c/air-force-1-07-essential-shoe-BHN3Db.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/490add03-5c99-403d-b456-48036981ac92/air-force-1-07-essential-shoe-BHN3Db.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/d4e9d5d6-3c97-4e58-bed6-1a2780519612/air-force-1-07-essential-shoe-BHN3Db.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/8222053d-ec2a-4ba9-a8bb-7fe7e2108dad/air-force-1-07-essential-shoe-BHN3Db.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/55111c5b-d5ea-4919-8d16-4af85bcdf0ae/air-force-1-07-essential-shoe-BHN3Db.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/ccf5f7e1-4a4c-460d-a8c4-a93f99050c50/air-force-1-07-essential-shoe-BHN3Db.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/7f0d8790-7309-4d95-96f1-280b2c3e5cf3/air-force-1-07-essential-shoe-BHN3Db.jpg"
      ],
      "Last Visited": "2020-04-13T15:27:56"
    },

```

### Find A Product

Find a product given the product id of the form `CT1726-100`.

#### POST

```
$ curl -X POST 'http://localhost:5000/products' -d '{"product_id": "CT1726-100"}' -H 'content-type: application/json' -H 'accept: application/json'
```

```json
{
  "products": [
    {
      "URL": "https://www.nike.com/in/t/court-vintage-shoe-bvP4d4/CT1726-100",
      "Product Name": "Nike Court Vintage Premium",
      "Product ID": "CT1726-100",
      "Listing Price": false,
      "Sale Price": 5495,
      "Discount": false,
      "Brand": "Nike",
      "Description": "The Nike Court Vintage Premium embodies '80s tennis at its best—laid-back and stylish. The smooth leather upper is combined with micro-branding for a relaxed look and feel, while the cushioned sockliner provides smooth comfort with every step.",
      "Rating": 0,
      "Reviews": 0,
      "Images": [
        "https://static.nike.com/a/images/t_PDP_1728_v1/de317847-20e7-48a5-93a9-36295235e4cf/court-vintage-shoe-bvP4d4.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/2aa34ff6-9aad-4e4a-a2c2-ca6b0e83e0f0/court-vintage-shoe-bvP4d4.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/aa2c8926-694a-4f9e-8b54-d9e3ce8de66a/court-vintage-shoe-bvP4d4.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/c793c818-8f9c-46d1-a5e3-84471c0d582a/court-vintage-shoe-bvP4d4.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/e5942a81-6e02-438d-9e94-c41f46c194b7/court-vintage-shoe-bvP4d4.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/d6bec5db-5f64-40d3-b6a7-1a094635d0c0/court-vintage-shoe-bvP4d4.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/fc7dca73-b62f-4a76-b9f0-f4710ffa435b/court-vintage-shoe-bvP4d4.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/7975795f-c2b7-4465-837b-bd191cc049db/court-vintage-shoe-bvP4d4.jpg"
      ],
      "Last Visited": "2020-04-13T15:28:04"
    }
  ]
}
```


#### GET

````
    $ curl 'http://localhost:5000/products/item/CT1726-100' -H 'accept: application/json'
```

```json
{
  "products": [
    {
      "URL": "https://www.nike.com/in/t/court-vintage-shoe-bvP4d4/CT1726-100",
      "Product Name": "Nike Court Vintage Premium",
      "Product ID": "CT1726-100",
      "Listing Price": false,
      "Sale Price": 5495,
      "Discount": false,
      "Brand": "Nike",
      "Description": "The Nike Court Vintage Premium embodies '80s tennis at its best—laid-back and stylish. The smooth leather upper is combined with micro-branding for a relaxed look and feel, while the cushioned sockliner provides smooth comfort with every step.",
      "Rating": 0,
      "Reviews": 0,
      "Images": [
        "https://static.nike.com/a/images/t_PDP_1728_v1/de317847-20e7-48a5-93a9-36295235e4cf/court-vintage-shoe-bvP4d4.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/2aa34ff6-9aad-4e4a-a2c2-ca6b0e83e0f0/court-vintage-shoe-bvP4d4.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/aa2c8926-694a-4f9e-8b54-d9e3ce8de66a/court-vintage-shoe-bvP4d4.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/c793c818-8f9c-46d1-a5e3-84471c0d582a/court-vintage-shoe-bvP4d4.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/e5942a81-6e02-438d-9e94-c41f46c194b7/court-vintage-shoe-bvP4d4.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/d6bec5db-5f64-40d3-b6a7-1a094635d0c0/court-vintage-shoe-bvP4d4.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/fc7dca73-b62f-4a76-b9f0-f4710ffa435b/court-vintage-shoe-bvP4d4.jpg",
        "https://static.nike.com/a/images/t_PDP_1728_v1/7975795f-c2b7-4465-837b-bd191cc049db/court-vintage-shoe-bvP4d4.jpg"
      ],
      "Last Visited": "2020-04-13T15:28:04"
    }
  ]
}
```

### POST




