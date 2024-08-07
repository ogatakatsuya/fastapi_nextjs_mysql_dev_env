"use client";

import { useState, useEffect } from 'react'
import Image from "next/image";
import { 
    Card,
    CardBody,
    Text,
    Box,
    Avatar,
    Flex,
    IconButton,
    useDisclosure,
} from '@chakra-ui/react'
import { FaRegCommentDots } from "react-icons/fa";
import CommentModal from './ReplyModal';
import LikeButton from './LikeButton';

const Post = ({ post_id }) => {
    const [ post, setPost ] = useState("");
    const { isOpen, onOpen, onClose } = useDisclosure()
    
    const fetchPost = async () => {
        const endpointUrl= process.env.NEXT_PUBLIC_BACKEND_ENDPOINT_URL
        const res = await fetch(`${endpointUrl}/post/${post_id}`)
        if(res.ok){
            const data = await res.json();
            setPost(data);
        }
    }

    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = (`0${date.getMonth() + 1}`).slice(-2);
        const day = (`0${date.getDate()}`).slice(-2);
        const hours = (`0${date.getHours()}`).slice(-2);
        const minutes = (`0${date.getMinutes()}`).slice(-2);
        return `${year}/${month}/${day} ${hours}:${minutes}`;
    };

    useEffect(() => {
        fetchPost();
    }, [])
    return (
        <>
            <Card width="500px" bgColor="gray.100">
                <CardBody>
                    <Flex alignItems="center">
                        <Avatar src={post?.icon_url}/>
                        <Box ml={3}>
                            <Text fontSize='md'>
                                {post.user_nickname ? post.user_nickname : post.user_name}
                            </Text>
                            <Text fontSize='xs'>
                                {formatDate(new Date(post.created_at))}
                            </Text>
                        </Box>
                    </Flex>
                    <Box>
                        <Text mt='4' fontSize='md'>
                            {post.text}
                        </Text>
                        {post.file_url &&
                            <Image
                                    src={post.file_url}
                                    width={200}
                                    height={200}
                                    alt="Imege"
                                    style={{ width: 'auto', height: 'auto' }}
                                    priority
                            />
                        }
                    </Box>
                    <Flex 
                        justifyContent="flex-end" 
                        alignItems="flex-end"
                        style={{ position: 'absolute', bottom: '10px', right: '10px' }}
                    >
                        <LikeButton post_id={post_id}/>
                        <IconButton 
                            icon={<FaRegCommentDots />}
                            aria-label="Comment Button"
                            onClick={onOpen}
                            size="sm"
                        />
                    </Flex>
                </CardBody>
            </Card>
            <Flex justifyContent="center" mt="5">
                <Text class>Comments</Text>
            </Flex>
            <CommentModal onClose={onClose} isOpen={isOpen} post_id={post_id}/>
        </>
    )
}

export default Post;