import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from search.models import Book
from my_profile.models import SearchHistory

class BookRecommender:
    def __init__(self, user):
        self.user = user
        self.model = None
        self.encoder = LabelEncoder()

    def _get_user_features(self):
        """
        核心逻辑：从数据库提取该用户的特征
        原理：分析用户的搜索历史，提取出他偏好的‘类型(subject)’
        """
        history = SearchHistory.objects.filter(user=self.user)
        if not history.exists():
            return None
        
        # 将搜索历史转化为 DataFrame 进行特征工程
        df_history = pd.DataFrame(list(history.values('browse_books')))
        # 这里假设 browse_books 存储的是书名或类型，简单处理为计数
        preference = df_history['browse_books'].value_counts().to_dict()
        return preference

    def _prepare_book_data(self):
        """
        将数据库中的书籍数据转化为模型可识别的矩阵（DataFrame）
        """
        books = Book.objects.all()
        df_books = pd.DataFrame(list(books.values(
            'id', 'price', 'rating', 'subject', 'reviewers'
        )))
        
        # 将分类数据(subject)数字化，因为机器学习模型不认识中文/英文单词
        df_books['subject_code'] = self.encoder.fit_transform(df_books['subject'])
        return df_books

    def train_and_predict(self):
        """
        推荐逻辑：加载/训练模型并预测
        """
        user_pref = self._get_user_features()
        df_books = self._prepare_book_data()
        
        if user_pref is None:
            # 冷启动：如果用户没历史，就推荐评分最高的（简单线性回归思想）
            return Book.objects.order_by('-rating')[:10]

        # 构造预测特征：书的特征 + 用户偏好匹配度
        # 这里简化处理：预测分数 = 基础分(rating) + XGBoost调整分
        X = df_books[['price', 'rating', 'subject_code', 'reviewers']]
        
        # 实际项目中这里应加载预训练好的 XGBoost 模型
        # bst = xgb.Booster()
        # bst.load_model('book_model.json')
        # preds = bst.predict(xgb.DMatrix(X))
        
        # 演示逻辑：暂时用简单的分值排序模拟
        df_books['score'] = df_books['rating'] * 0.7 + df_books['reviewers'] * 0.3
        
        # 排序并取前10个ID
        recommended_ids = df_books.sort_values(by='score', ascending=False)['id'].head(10).tolist()
        return Book.objects.filter(id__in=recommended_ids)