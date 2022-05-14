const express = require('express');
const router = express.Router();

const { Like } = require('../models/Like');
const { Dislike } = require('../models/Dislike');

//=============================
//           Likes
//=============================

router.post('/getLikes', (req, res) => {

    let variable = {}

    if(req.body.postId){
        variable = { postId: req.body.postId }
    } else {
        variable = { commentId: req.body.commentId }
    }

    Like.find(variable)
    .exec((err, likes) => {
        if(err) return res.status(400).send(err)
        res.status(200).json({success: true, likes})
    })
})


router.post('/getDislikes', (req, res) => {

    let variable = {}

    if(req.body.postId){
        variable = { postId: req.body.postId }
    } else {
        variable = { commentId: req.body.commentId }
    }

    Dislike.find(variable)
    .exec((err, dislikes) => {
        if(err) return res.status(400).send(err)
        res.status(200).json({success: true, dislikes})
    })
})


router.post('/upLike', (req, res) => {

    let variable = {}

    if(req.body.postId){
        variable = { postId: req.body.postId, userId: req.body.userId}
    } else {
        variable = { commentId: req.body.commentId, userId: req.body.userId }
    }
    //like 콜렉션에 클릭정보 넣어줌.
    const like =new Like(variable)
    like.save((err, likeResult) => {
        if(err) return res.json({ success: false, err })

        // 싫어요가 눌러져있다면, 좋아요 증가 동시에 기존의 싫어요 감소
        Dislike.findOneAndDelete(variable)
        .exec((err, dislikeResult) => {
            if(err) return res.status(400).json({success: false, err})
            res.status(200).json({ success: true })
        })
    })
})

router.post('/unLike', (req, res) => {

    let variable = {}

    if(req.body.postId){
        variable = { postId: req.body.postId, userId: req.body.userId}
    } else {
        variable = { commentId: req.body.commentId, userId: req.body.userId }
    }

    Like.findOneAndDelete(variable)
    .exec((err, result) => {
        if(err) return res.status(400).json({ success: false, err })
        res.status(200).json({ success: true })
    })
})


router.post('/upDislike', (req, res) => {

    let variable = {}

    if(req.body.postId){
        variable = { postId: req.body.postId, userId: req.body.userId}
    } else {
        variable = { commentId: req.body.commentId, userId: req.body.userId }
    }
    //like 콜렉션에 클릭정보 넣어줌.
    const dislike =new Dislike(variable)
    dislike.save((err, dislikeResult) => {
        if(err) return res.json({ success: false, err })

        // 싫어요가 눌러져있다면, 좋아요 증가 동시에 기존의 싫어요 감소
        Like.findOneAndDelete(variable)
        .exec((err, likeResult) => {
            if(err) return res.status(400).json({success: false, err})
            res.status(200).json({ success: true })
        })
    })
})


router.post('/unDislike', (req, res) => {

    let variable = {}

    if(req.body.postId){
        variable = { postId: req.body.postId, userId: req.body.userId}
    } else {
        variable = { commentId: req.body.commentId, userId: req.body.userId }
    }

    Dislike.findOneAndDelete(variable)
    .exec((err, result) => {
        if(err) return res.status(400).json({ success: false, err })
        res.status(200).json({ success: true })
    })
})




module.exports = router;