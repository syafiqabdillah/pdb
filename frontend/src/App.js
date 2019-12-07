import React from 'react';
import axios from 'axios';
import {
  Navbar, NavbarBrand, Container, Row, Col, Card,
  CardBody, CardHeader, Form, Input, Label, FormGroup, Button,
} from 'reactstrap';
import {
  PieChart, Pie, Cell, Sector, Line,
  Radar, RadarChart, PolarGrid, Legend,
  PolarAngleAxis, PolarRadiusAxis,
} from 'recharts';



const COLORS = ['#fa4252', '#46b3e6'];

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      loaded: false,
      fighter_name: null,
      fighter_lawan: null,
      fighter_saya: null,
      data_saya: null,
      data_lawan: null
    }

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.detailFighter = this.detailFighter.bind(this);
  }

  static jsfiddleUrl = 'https://jsfiddle.net/alidingling/90v76x08/';

  render() {
    let data_lawann;
    let chart1;
    if (this.state.loading) {
      chart1 = <div align="center">Loading...</div>
    } else {
      if (this.state.loaded) {
        data_lawann = [
          {
            "name": "Red",
            "value": this.state.data_lawan.red
          },
          {
            "name": "Blue",
            "value": this.state.data_lawan.blue
          }
        ]

        chart1 = (
          <PieChart width={800} height={400} onMouseEnter={this.onPieEnter}>
            <Pie
              data={data_lawann}
              cx={250}
              cy={150}
              innerRadius={60}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
              nameKey="name"
              label={({
                cx,
                cy,
                midAngle,
                innerRadius,
                outerRadius,
                name,
                value,
                index
              }) => {
                const RADIAN = Math.PI / 180;
                // eslint-disable-next-line
                const radius = 25 + innerRadius + (outerRadius - innerRadius);
                // eslint-disable-next-line
                const x = cx + radius * Math.cos(-midAngle * RADIAN);
                // eslint-disable-next-line
                const y = cy + radius * Math.sin(-midAngle * RADIAN);

                return (
                  <text
                    x={x}
                    y={y}
                    fill="#000000"
                    textAnchor={x > cx ? "start" : "end"}
                    dominantBaseline="central"
                  >
                    {name} ({value})
                  </text>
                );
              }}
            >
              {
                data_lawann.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)
              }
            </Pie>
            <Legend />
          </PieChart>
        );
      } else {
        chart1 = "";
      }
    }

    let data2;
    let chart2;

    if (this.state.loading) {
      chart2 = <div align="center">Loading...</div>
    } else {
      if (this.state.loaded) {
        let perf_saya = this.state.saya;
        let perf_lawan = this.state.lawan;
        let perf_avg = this.state.avg;
        let fighter_saya = this.state.fighter_saya;
        let fighter_lawan = this.state.fighter_lawan;
        data2 = [
          {
            "subject": 'Distance Landed', "Anda": perf_saya.distance, "Lawan": perf_lawan.distance, "Average": perf_avg.distance, "fullMark": perf_avg.distance,
          },
          {
            "subject": 'Ground Landed', "Anda": perf_saya.ground, "Lawan": perf_lawan.ground, "Average": perf_avg.ground, "fullMark": perf_avg.ground,
          },
          {
            "subject": 'Head Landed', "Anda": perf_saya.head, "Lawan": perf_lawan.head, "Average": perf_avg.head, "fullMark": perf_avg.head,
          },
          {
            "subject": 'Leg Landed', "Anda": perf_saya.leg, "Lawan": perf_lawan.leg, "Average": perf_avg.leg, "fullMark": perf_avg.leg,
          },
          {
            "subject": 'Body Landed', "Anda": perf_saya.body, "Lawan": perf_lawan.body, "Average": perf_avg.body, "fullMark": perf_avg.body,
          },
        ];

        chart2 = (
          <RadarChart cx={250} cy={200} outerRadius={125} width={500} height={400} data={data2}>
            <PolarGrid />
            <PolarAngleAxis dataKey="subject" />
            <PolarRadiusAxis angle={30} domain={[0, 30]} />
            <Radar dataKey="Anda" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
            <Radar dataKey="Lawan" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
            <Radar dataKey="Average" stroke="#e9ea77" fill="#e9ea77" fillOpacity={0.6} />
            <Legend />
          </RadarChart>
        );
      } else {
        chart2 = "";
      }
    }


    let select_name;
    if (this.state.fighter_name !== null) {
      select_name = this.state.fighter_name.map((fighter, index) => <option key={index}>{fighter}</option>);
    } else {
      select_name = "";
    }

    let button_detail_fighter;
    if (this.state.fighter_lawan){
      button_detail_fighter = (
        <Button color="info" block onClick={this.detailFighter}>DETAIL LAWAN</Button>
      );
    } else {
      button_detail_fighter = (
        <Button color="secondary" block onClick={this.detailFighter} disabled>DETAIL LAWAN</Button>
      );
    }

    return (
      <div>
        <Navbar color="light" light>
          <NavbarBrand href="/">UFC Dashboard Using Apache Drill</NavbarBrand>
        </Navbar>
        <Container className="mt-3">
          <div align="center">
            <h2>Fight Smarter with Us </h2>
          </div>

          <Form>
            <Row form>
              <Col md={6}>
                <FormGroup>
                  <Label for="pilihSaya">Nama Fighter Anda</Label>
                  <Input type="select" name="fighter_saya" id="pilihSaya" onChange={this.handleInputChange}>
                    {select_name}
                  </Input>
                </FormGroup>
              </Col>
              <Col md={6}>
                <FormGroup>
                  <Label for="pilihLawan">Nama Fighter Lawan</Label>
                  <Input type="select" name="fighter_lawan" id="pilihLawan" onChange={this.handleInputChange}>
                    {select_name}
                  </Input>
                </FormGroup>
              </Col>
            </Row>
            <Row form>
              <Button color="info" block onClick={this.handleSubmit}>ANALISIS</Button>
            </Row>
            <hr></hr>
            <Row form>
              {button_detail_fighter}
            </Row>
          </Form>
          <hr />
          <Row>
            <Col md={6}>
              <Card>
                <CardHeader>Jumlah Menang Lawan Berdasarkan Sisi</CardHeader>
                <CardBody>
                  {chart1}
                </CardBody>
              </Card>
            </Col>
            <Col md={6}>
              <Card>
                <CardHeader>Perbandingan Performa Anda vs Lawan</CardHeader>
                <CardBody>
                  {chart2}
                </CardBody>
              </Card>
            </Col>
          </Row>
        </Container>
      </div>
    );
  }

  detailFighter(e){
    e.preventDefault();
    axios.get("http://localhost:5000/fighter-detail/" + this.state.fighter_lawan)
    .then(res => {
      const data = res.data;
    alert(this.state.fighter_lawan + " : Height " + data.height + " - Weight " + data.weight + ' - Stance ' + data.stance + ' - Reach ' + data.reach);
    })
  }

  handleInputChange(event) {
    const target = event.target;
    const name = target.name;
    this.setState({
      [name]: target.value
    });
  }

  handleSubmit(e) {
    e.preventDefault();
    if (this.state.fighter_saya == null || this.state.fighter_lawan == null) {
      alert("lengkapi form");
    } else {
      this.setState({
        loading: true
      });
      axios.get('http://localhost:5000/compare/' + this.state.fighter_saya + '/' + this.state.fighter_lawan)
        .then(res => {
          this.setState({
            saya: res.data.radar.saya,
            lawan: res.data.radar.lawan,
            avg: res.data.radar.average,
            loading: false,
            loaded: true,
            data_saya: res.data.pie.saya,
            data_lawan: res.data.pie.lawan,
          })
        })
    }
  }

  componentDidMount() {
    axios.get('http://localhost:5000/fighter-name')
      .then(res => {
        this.setState({
          fighter_name: res.data.sort()
        })
      })
  }

}


