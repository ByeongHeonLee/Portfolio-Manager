// axios.get(`api/data/dataId?id`)
router.get("/data_id", (req, res) => {
    let type = req.query.type;
    let dataId = req.query.id;
  
    Data.find({ _id: dataId })
      .populate("title")
      .exec((err, data) => {
        if (err) return res.status(400).send(err);
        return res.status(200).send({ success: true, data });
      });
  });