import React from 'react';
import { FullPage, Slide } from 'react-full-page';
import { Icon, Button } from 'antd';
import './FullPage.css'
import man_img from '../../../images/character.png'
import kospi_img from '../../../images/kospi_img.png'
import kosdaq_img from '../../../images/kosdaq_img.png'
import krx_img from '../../../images/krx_img.png'

export default class fullPage extends React.Component {
  render() {
    return (
        <div className='full-page'>
          <FullPage controls controlsProps={{className: 'slide-navigation'}}>
              <Slide>
              <div className="section-common section-area1">
                <h1>Portfolio.com</h1>
                <img src={man_img} className='man_img'></img>
              </div>
              </Slide>
              <Slide>
              <div className="section-common section-area2">
                <div className='search_bar'>
                  <h1>삼성전자</h1>
                </div>
                <Button type="primary" size="large" href="/search" 
                  style={{ border: '1px solid rgb(0, 88, 202)', backgroundColor:'rgb(0, 88, 202)', color: 'white', top: '75%', left: '70%',
                  borderRadius: '20px', padding: '8px', height:'60px', width: '200px', fontSize: '20px', fontWeight: 'bolder' }}>
                    종목 검색하기</Button>
              </div>
              </Slide>
              <Slide>
              <div className="section-common section-area3">
                <img src={kospi_img} className='kospi_img'></img>
                <img src={kosdaq_img} className='kosdaq_img'></img>
                <img src={krx_img} className='krx_img'></img>
                <Button type="primary" size="large" href="/index" 
                  style={{ border: '1px solid rgb(0, 88, 202)', backgroundColor:'rgb(0, 88, 202)', color: 'white', top: '75%',
                  borderRadius: '20px', padding: '8px', height:'60px', width: '200px', fontSize: '20px', fontWeight: 'bolder' }}>
                    지수 확인하기</Button>
              </div>
              </Slide>
              <Slide>
              <div className="section-common section-area4">
                4
              </div>
              </Slide>
              <Slide>
              <div className="section-common section-area5">
                5
              </div>
              </Slide>
          </FullPage>
        </div>
    );
  }
};
