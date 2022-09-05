import React from "react";
import { Descriptions } from "antd";

function DataInfo(props) {
  return (
    <div>
      <Descriptions title="종목상세정보" bordered>
        <Descriptions.Item label="corpNm">
          {props.detailData.corpNm}
        </Descriptions.Item>
        <Descriptions.Item label="corpEnsnNm">
          {props.detailData.corpEnsnNm}
        </Descriptions.Item>
        <Descriptions.Item label="homepAddr">
          {props.detailData.homepAddr}
        </Descriptions.Item>
        <Descriptions.Item label="shotnIsin">
          {props.detailData.shotnIsin}
        </Descriptions.Item>
      </Descriptions>
    </div>
  );
}

export default DataInfo;