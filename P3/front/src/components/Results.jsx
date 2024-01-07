import React from 'react';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import { Rating } from 'primereact/rating';

export default function Results({ productos }) {
  return (
    <div className="container text-center">
      <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 justify-content-center" style={{ marginTop: '60px' }}>
        {productos.map((producto) => (
          <div className="col mb-4" key={producto.id}>

            <Card className="h-100">
            <Card.Img variant="top" src={`${producto.image}`} style={{ maxWidth: '100%', height: '400px' }} alt="..." />


              <Card.Body style={{ maxWidth: '100%' }}>
                <Card.Title>{producto.title}</Card.Title>

                <Button
                  variant="dark" type="button" data-bs-toggle="collapse" data-bs-target={`#description${producto.id}`}
                  aria-expanded="false" aria-controls={`description${producto.id}`}
                  style={{ backgroundColor: '#9370DB', marginBottom: '10px' }}
                >
                  Description
                </Button>

                <div className="collapse" id={`description${producto.id}`}>
                  <p className="card-text">{producto.description}</p>
                </div>

                <div className="container" style={{ marginTop: '20px' }}>
                  <p className="card-text">{producto.price} €</p>
                  <Button variant="primary">Buy</Button>
                </div>

                <div className="d-flex flex-column align-items-center" style={{ marginTop: '20px' }}>

                  <div style={{ textAlign: 'center' }}>
                    <span className="sp" data-product-id={producto.id}></span>
                    <p className="text-success font-weight-bold" style={{ fontFamily: 'Arial, sans-serif' }}>
                      Rating: {producto.rating.rate}
                    </p>
                    <p className="text-success font-weight-bold" style={{ fontFamily: 'Arial, sans-serif' }}>
                      Number of rates: {producto.rating.count}
                    </p>
                  </div>

                  <div className="d-flex justify-content-center align-items-center">
                    <Rating value={producto.rating.rate} readOnly cancel={false} />
                  </div>

                </div>
              </Card.Body>
            </Card>
          </div>
        ))}
      </div>
    </div>
  );
}