const renderCard = Datas.map((data, index) => {
    return (
      <div style={{ display: "Grid", placeItems: "center" }}>
        <Col lg={4} md={6} xs={16} key={index}>
          <Card
            style={{
              width: "350px",
              height: "20%",
              position: "relative",
              right: "50%",
            }}
           //추가
            cover={
              <a href={`/reveiw/data/${data._id}`}>
                <ImageSlider images={data.images} />
              </a>
            }
          >
            <Meta title={data.title} description={`$${data.price}`}></Meta>
          </Card>
        </Col>
      </div>
    );
  });