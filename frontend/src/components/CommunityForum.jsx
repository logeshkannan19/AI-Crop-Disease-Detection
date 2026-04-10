import React, { useState, useEffect } from 'react';

const CommunityForum = ({ isLoggedIn }) => {
  const [posts, setPosts] = useState([
    { id: 1, title: 'How to prevent tomato late blight?', content: 'My tomato plants are showing signs of late blight. What preventive measures can I take?', category: 'question', crop: 'Tomato', author: 'FarmerJohn', likes: 12, comments: 5, time: '2 hours ago' },
    { id: 2, title: 'Successfully treated corn rust!', content: 'After 3 weeks of treatment, my corn is now healthy. Here is what worked for me...', category: 'success_story', crop: 'Corn', author: 'AgriPro', likes: 45, comments: 23, time: '5 hours ago' },
    { id: 3, title: 'Best fungicides for potato early blight', content: 'Comparing different fungicides and their effectiveness on early blight...', category: 'tip', crop: 'Potato', author: 'CropExpert', likes: 28, comments: 14, time: '1 day ago' }
  ]);
  const [activeTab, setActiveTab] = useState('all');
  const [showCreate, setShowCreate] = useState(false);
  const [newPost, setNewPost] = useState({ title: '', content: '', category: 'discussion', crop: '' });
  const [search, setSearch] = useState('');

  const categories = [
    { id: 'all', name: 'All', icon: '📋' },
    { id: 'discussion', name: 'Discussion', icon: '💬' },
    { id: 'question', name: 'Questions', icon: '❓' },
    { id: 'tip', name: 'Tips', icon: '💡' },
    { id: 'success_story', name: 'Success', icon: '🏆' }
  ];

  const filteredPosts = posts.filter(post => {
    if (activeTab !== 'all' && post.category !== activeTab) return false;
    if (search && !post.title.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  const handleCreate = (e) => {
    e.preventDefault();
    if (!isLoggedIn) {
      alert('Please login to post');
      return;
    }
    const post = {
      id: Date.now(),
      ...newPost,
      author: 'You',
      likes: 0,
      comments: 0,
      time: 'Just now'
    };
    setPosts([post, ...posts]);
    setShowCreate(false);
    setNewPost({ title: '', content: '', category: 'discussion', crop: '' });
  };

  const handleLike = (id) => {
    setPosts(posts.map(p => p.id === id ? { ...p, likes: p.likes + 1 } : p));
  };

  return (
    <div className="forum">
      <div className="forum-header">
        <h3>🌐 Community Forum</h3>
        <button className="create-post-btn" onClick={() => setShowCreate(true)}>+ New Post</button>
      </div>

      <div className="forum-search">
        <input type="text" placeholder="Search discussions..." value={search} onChange={e => setSearch(e.target.value)} />
      </div>

      <div className="forum-categories">
        {categories.map(cat => (
          <button key={cat.id} className={activeTab === cat.id ? 'active' : ''} onClick={() => setActiveTab(cat.id)}>
            {cat.icon} {cat.name}
          </button>
        ))}
      </div>

      {showCreate && (
        <div className="create-modal">
          <form onSubmit={handleCreate}>
            <input type="text" placeholder="Post title" value={newPost.title} onChange={e => setNewPost({...newPost, title: e.target.value})} required />
            <textarea placeholder="Share your thoughts..." value={newPost.content} onChange={e => setNewPost({...newPost, content: e.target.value})} required />
            <select value={newPost.category} onChange={e => setNewPost({...newPost, category: e.target.value})}>
              <option value="discussion">💬 Discussion</option>
              <option value="question">❓ Question</option>
              <option value="tip">💡 Tip</option>
              <option value="success_story">🏆 Success Story</option>
            </select>
            <select value={newPost.crop} onChange={e => setNewPost({...newPost, crop: e.target.value})}>
              <option value="">Select Crop (optional)</option>
              <option value="Tomato">🍅 Tomato</option>
              <option value="Potato">🥔 Potato</option>
              <option value="Corn">🌽 Corn</option>
            </select>
            <div className="modal-actions">
              <button type="button" className="cancel-btn" onClick={() => setShowCreate(false)}>Cancel</button>
              <button type="submit" className="submit-btn">Post</button>
            </div>
          </form>
        </div>
      )}

      <div className="posts-list">
        {filteredPosts.map(post => (
          <div key={post.id} className="post-card">
            <div className="post-header">
              <span className={`category-badge ${post.category}`}>{post.category.replace('_', ' ')}</span>
              {post.crop && <span className="crop-tag">{post.crop}</span>}
              <span className="post-time">{post.time}</span>
            </div>
            <h4>{post.title}</h4>
            <p>{post.content.substring(0, 150)}...</p>
            <div className="post-footer">
              <span className="author">👤 {post.author}</span>
              <button className="like-btn" onClick={() => handleLike(post.id)}>
                ❤️ {post.likes}
              </button>
              <span className="comments">💬 {post.comments}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CommunityForum;
