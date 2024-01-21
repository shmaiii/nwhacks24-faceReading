import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import Webcam from 'react-webcam';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import 'bootstrap/dist/css/bootstrap.min.css';
import splash from './splash.gif';

function SplashScreen() {
  return (
    <div className="splash-screen">
      <img src={splash} alt="Splash" style={{ width: '100%', height: '100%', objectFit: 'cover' }}/>
    </div>
  );
}

function CapturePage({ onCapture }) {
  const webcamRef = React.useRef(null);
  const navigate = useNavigate();

  const captureHandler = async () => {
    const imageSrc = webcamRef.current.getScreenshot();

    try {
      const response = await fetch('YOUR_BACKEND_API_ENDPOINT', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageSrc }),
      });

      if (response.ok) {
        const resultData = await response.json();
        onCapture(resultData);
        navigate('/result');
      } else {
        console.error('Failed to process the image on the backend');
      }
    } catch (error) {
      console.error('Error while communicating with the backend', error);
    }
  };

  return (
    <Container>
      <Navbar>
        <Container>
          <Navbar.Brand as={Link} to="/">
            Face Reading
          </Navbar.Brand>
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">
              Detect
            </Nav.Link>
            <Nav.Link as={Link} to="/result">
              Result
            </Nav.Link>
          </Nav>
        </Container>
      </Navbar>

      <Form className="mt-3 text-center">
        <Form.Group className="mb-3 text-center">
          <Webcam ref={webcamRef} />
        </Form.Group>
        <Form.Group className="mb-3 text-center">
          <Button variant="primary" onClick={captureHandler} className="mb-3">
            Capture
          </Button>
        </Form.Group>
      </Form>
    </Container>
  );
}

function ResultPage({ resultData }) {
  return (
    <Container>
      <Navbar>
        <Container>
          <Navbar.Brand as={Link} to="/">
            Face Reading
          </Navbar.Brand>
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">
              Detect
            </Nav.Link>
            <Nav.Link as={Link} to="/result">
              Result
            </Nav.Link>
          </Nav>
        </Container>
      </Navbar>

      <div className="mt-3 text-center">
        <h2>Result</h2>
        {resultData.image && <img src={resultData.image} alt="Result" className="mb-3" />}
        <p>{resultData.additionalInfo}</p>
      </div>
    </Container>
  );
}

function App() {
  const [resultData, setResultData] = useState(null);
  const [showSplash, setShowSplash] = useState(true);

  useEffect(() => {
    const splashTimeout = setTimeout(() => {
      setShowSplash(false);
    }, 3000);

    return () => clearTimeout(splashTimeout);
  }, []);

  return (
    <Router>
      {showSplash ? (
        <SplashScreen />
      ) : (
        <Routes>
          <Route path="/" element={<CapturePage onCapture={setResultData} />} />
          <Route
            path="/result"
            element={
              resultData ? (
                <ResultPage resultData={resultData} />
              ) : (
                <Navigate to="/" />
              )
            }
          />
        </Routes>
      )}
    </Router>
  );
}

export default App;
